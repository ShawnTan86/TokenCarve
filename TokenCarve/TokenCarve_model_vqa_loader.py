import argparse
import torch
import os
import json
from tqdm import tqdm
import shortuuid
import torch.profiler
# from fvcore.nn import FlopCountAnalysis
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.conversation import conv_templates, SeparatorStyle
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from llava.mm_utils import tokenizer_image_token, process_images, get_model_name_from_path
from torch.utils.data import Dataset, DataLoader

from PIL import Image
import math


def split_list(lst, n):
    """Split a list into n (roughly) equal-sized chunks"""
    chunk_size = math.ceil(len(lst) / n)  # integer division
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]


def get_chunk(lst, n, k):
    chunks = split_list(lst, n)
    return chunks[k]


# Custom dataset class
class CustomDataset(Dataset):
    def __init__(self, questions, image_folder, tokenizer, image_processor, model_config):
        self.questions = questions
        self.image_folder = image_folder
        self.tokenizer = tokenizer
        self.image_processor = image_processor
        self.model_config = model_config

    def __getitem__(self, index):
        line = self.questions[index]
        image_file = line["image"]
        qs = line["text"]
        if self.model_config.mm_use_im_start_end:
            qs = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + qs
        else:
            qs = DEFAULT_IMAGE_TOKEN + '\n' + qs

        conv = conv_templates[args.conv_mode].copy()
        conv.append_message(conv.roles[0], qs)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        image = Image.open(os.path.join(self.image_folder, image_file)).convert('RGB')
        image_tensor = process_images([image], self.image_processor, self.model_config)[0]

        input_ids = tokenizer_image_token(prompt, self.tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt')

        return input_ids, image_tensor, image.size

    def __len__(self):
        return len(self.questions)


def collate_fn(batch):
    input_ids, image_tensors, image_sizes = zip(*batch)
    input_ids = torch.stack(input_ids, dim=0)
    image_tensors = torch.stack(image_tensors, dim=0)
    return input_ids, image_tensors, image_sizes


# DataLoader
def create_data_loader(questions, image_folder, tokenizer, image_processor, model_config, batch_size=1, num_workers=4):
    assert batch_size == 1, "batch_size must be 1"
    dataset = CustomDataset(questions, image_folder, tokenizer, image_processor, model_config)
    data_loader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False, collate_fn=collate_fn)
    return data_loader

    
def eval_model(args):
    # Model
    disable_torch_init()
    model_path = os.path.expanduser(args.model_path)
    model_name = get_model_name_from_path(model_path)
    tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, args.model_base, model_name)
    questions = [json.loads(q) for q in open(os.path.expanduser(args.question_file), "r")]
    questions = get_chunk(questions, args.num_chunks, args.chunk_idx)
    answers_file = os.path.expanduser(args.answers_file)
    os.makedirs(os.path.dirname(answers_file), exist_ok=True)
    ans_file = open(answers_file, "w")
    print(ans_file)

    if 'plain' in model_name and 'finetune' not in model_name.lower() and 'mmtag' not in args.conv_mode:
        args.conv_mode = args.conv_mode + '_mmtag'
        print(f'It seems that this is a plain model, but it is not using a mmtag prompt, auto switching to {args.conv_mode}.')

    data_loader = create_data_loader(questions, args.image_folder, tokenizer, image_processor, model.config)

    ################# token_carve parameter start
    model.config.use_token_carve = args.use_token_carve
    model.config.token_carve_sys_length = args.token_carve_sys_length
    model.config.token_carve_image_token_length = args.token_carve_image_token_length
    model.config.token_carve_work_layer = args.token_carve_work_layer
    model.config.token_carve_image_token_rank = int(args.token_carve_image_token_nums / 2 * 3)
    model.config.token_carve_merge_token_nums = int(args.token_carve_image_token_nums / 2)
    model.config.token_carve_SV_AV_mode = args.token_carve_SV_AV_mode
    model.config.token_carve_SV_AV_weight = args.token_carve_SV_AV_weight

    ## parameter reset
    model.model.reset_token_carve_parameter()
    ################# token_carve parameter ending
    
    print('model.config.token_carve_sys_length: {}'.format(model.config.token_carve_sys_length))
    current_model = model
    while hasattr(current_model, "LlamaModel"):
        current_model = current_model.base_model
        print(type(current_model), type(current_model).__module__)

    for (input_ids, image_tensor, image_sizes), line in tqdm(zip(data_loader, questions), total=len(questions)):
        idx = line["question_id"]
        cur_prompt = line["text"]

        input_ids = input_ids.to(device='cuda', non_blocking=True)

        with torch.inference_mode():
            output_ids = model.generate(
                input_ids,
                images=image_tensor.to(dtype=torch.float16, device='cuda', non_blocking=True),
                image_sizes=image_sizes,
                do_sample=True if args.temperature > 0 else False,
                temperature=args.temperature,
                top_p=args.top_p,
                num_beams=args.num_beams,
                max_new_tokens=args.max_new_tokens,     
                output_attentions=True,
                use_cache=True)

        outputs = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
        ans_id = shortuuid.uuid()
        ans_file.write(json.dumps({"question_id": idx,
                                   "prompt": cur_prompt,
                                   "text": outputs,
                                   "answer_id": ans_id,
                                   "model_id": model_name,
                                   "metadata": {}}) + "\n")
    ans_file.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="./llava7b")
    parser.add_argument("--model-base", type=str, default=None)
    parser.add_argument("--image-folder", type=str, default="./playground/data/eval/textvqa/train_images")
    parser.add_argument("--question-file", type=str, default="./playground/data/eval/textvqa/llava_textvqa_val_v051_ocr.jsonl")
    parser.add_argument("--answers-file", type=str, default="./TokenCarve_llava-v1.5-7b.jsonl")
    parser.add_argument("--conv-mode", type=str, default="vicuna_v1")
    parser.add_argument("--num-chunks", type=int, default=1)
    parser.add_argument("--chunk-idx", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--top_p", type=float, default=None)
    parser.add_argument("--num_beams", type=int, default=1)
    parser.add_argument("--max_new_tokens", type=int, default=128)

    ################# token_carve parameter start
    parser.add_argument("--use-token-carve", default=False, action='store_true') # use TokenCarve
    parser.add_argument('--token-carve-sys-length', type=int, default=36)
    parser.add_argument('--token-carve-image-token-length', type=int, default=576)
    parser.add_argument('--token-carve-work-layer', type=int, default=2)
    parser.add_argument('--token-carve-image-token-nums', type=int, default=64) # Set the number of image tokens
    parser.add_argument('--token-carve-SV-AV-mode', type=int, default=0)    # 0:TokenCarve mode, 1:SV mode, 2: AV mode  
    parser.add_argument('--token-carve-SV-AV-weight', type=float, default=0.5) # Weight of SV to AV
    ################# token_carve parameter ending

    args = parser.parse_args()
    print(args)
    eval_model(args)

