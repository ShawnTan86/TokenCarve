# TokenCarve: Information-Preserving Visual Token Compression in Multimodal Large Language Models

If you have any questions, please contact Xudong Tan(shawntan@126.com).

## News

🌟 **[2025/3/13]** Our work is now available on [arXiv](https://arxiv.org/abs/2503.10501)!

---

## Contents

- [News](#news)
- [Contents](#contents)
- [Overview](#overview)
- [Usage](#usage)
- [Citation](#citation)

---

## Overview

### Figure 1
![Figure 1](https://github.com/ShawnTan86/TokenCarve/blob/main/lmagesFolderForReadMe/Figure_1.png)
**Description:** (a) The radar chart illustrates the performance of TokenCarve on eight datasets when compressing the visual tokens of LLaVA1.5-7B from 576 to 192, showing that the overall performance remains close to the uncompressed version despite the significant token reduction; (b) Key performance indicators demonstrate that TokenCarve achieves a compression ratio of 77.8\%, with an average performance drop of only 1.54\%, a 1.23× inference speedup, and a 64\% reduction in KV cache usage; (c) The visualization depicts token positions during the two-stage compression process, where gray tokens are pruned and pink tokens are merged. In this OCR task example, TokenCarve consistently focuses on the critical regions of the image containing the text "Hawaii" throughout all compression stages.

### Abstract
Multimodal Large Language Models (MLLMs)  are becoming increasingly popular, while the high computational cost associated with multimodal data input, particularly from visual tokens, poses a significant challenge. Existing training-based token compression methods improve inference efficiency but require costly retraining, while training-free methods struggle to maintain performance when aggressively reducing token counts. In this study, we reveal that the performance degradation of MLLM closely correlates with the accelerated loss of information in the attention output matrix. This insight introduces a novel information-preserving perspective, making it possible to maintain performance even under extreme token compression. Based on this finding, we propose TokenCarve, a training-free, plug-and-play, two-stage token compression framework. The first stage employs an Information-Preservation-Guided Selection (IPGS) strategy to prune low-information tokens, while the second stage further leverages IPGS to guide token merging, minimizing information loss. Extensive experiments on 11 datasets and 2 model variants demonstrate the effectiveness of TokenCarve. It can even reduce the number of visual tokens to 22.2% of the original count, achieving a 1.23× speedup in inference, a 64% reduction in KV cache storage, and only a 1.54% drop in accuracy.

### Figure 2
![Figure 2](https://github.com/ShawnTan86/TokenCarve/blob/main/lmagesFolderForReadMe/Figure_2.png)
**Description:** The pipeline of the proposed TokenCarve framework. TokenCarve is integrated between the second and third layers of the LLaVA-1.5 model as a plug-and-play module, effectuating visual token compression during the prefilling stage. The upper panel illustrates TokenCarve’s integration with LLaVA-1.5, which conventionally comprises 36 system tokens, 576 visual tokens, and a variable number of prompt tokens. The lower panel (the blue region on the left) details the two-stage compression process: Carving Stage I employs the IPGS module to excise tokens with low contribution; Carving Stage II implements finer-grained token merging based on GSM, maximizing information retention. The IPGS module (right region of the lower panel) calculates each token’s information contribution score and attention score, then combines the two into a final ranking score (a higher slash count indicates a higher information contribution, and darker tokens signify higher attention). The GSM module (middle region of the lower panel) uses these IPGS scores to split tokens into a higher-scored Set A and a lower-scored Set B, then merges Set B tokens with their most similar counterparts in Set A based on cosine similarity (with deeper connection lines representing higher similarity).

### Figure 3
![Figure 3](https://github.com/ShawnTan86/TokenCarve/blob/main/lmagesFolderForReadMe/Figure_3.png)
**Description:** In this section, we thoroughly analyze the visualization results of the TokenCarve method, which reduces the number of visual tokens from 576 down to 128. We conduct visualization experiments across three key tasks: Optical Character Recognition (OCR), reasoning, and hallucination. Comparisons are made with the original LLaVA model, where tokens remain uncompressed. In the OCR task, TokenCarve continues to distinctly focus on regions containing the necessary textual information after token compression. As illustrated above, the extracted text from TokenCarve is highly similar to that obtained by the original LLaVA model, and both methods accurately extract the target text. For the reasoning task, TokenCarve maintains attention on critical details mentioned in the prompt even after compressing tokens. Interestingly, the final answers from the TokenCarve model sometimes outperform those of the original uncompressed LLaVA model. In the hallucination task, TokenCarve consistently retains its attention on the key spatial details indicated by the prompt, avoiding hallucinations caused by token loss. Furthermore, the final responses from TokenCarve remain comparable to those generated by the original LLaVA model without token compression.

---

## Usage

Usage: LLaVA + TokenCarve

This is a usage example for the LLaVA version of TokenCarve.

🛠 Step 1: Install LLaVA

Follow the installation guide in the official ！[LLaVA](https://github.com/haotian-liu/LLaVA) repository.

📁 Step 2: Integrate TokenCarve into LLaVA

Place the TokenCarve_config directory into the root of your LLaVA folder. The resulting directory structure should look like this:

LLaVA/
├── TokenCarve_config/
│   ├── config.py
│   ├── configuration_llama.py
│   ├── modeling_llama.py
│   └── TokenCarve_model_vqa_loader.py
├── LICENSE
├── README.md
├── cog.yaml
├── docs/
├── images/
├── llava/
├── llava.egg-info/
├── playground/
├── predict.py
├── pyproject.toml
├── scripts/
└── ...


🐍 Step 3: Activate the LLaVA Conda Environment

conda activate llava

📂 Step 4: Navigate to the LLaVA Directory

cd LLaVA

⚙️ Step 5: Run the TokenCarve Configuration Script

python ./TokenCarve_config/config.py

This script sets up TokenCarve-specific configurations, such as copying customized model files.

🧪 Step 6: Run the VQA Loader Script

python ./TokenCarve_config/TokenCarve_model_vqa_loader.py

💡 You can modify the token_carve_image_token_nums parameter to control how many image tokens are used in computation.

---

## Citation

If you use our code for your paper, please cite:

```bibtex
@misc{tan2025tokencarve,
  title={TokenCarve: Information-Preserving Visual Token Compression in Multimodal Large Language Models},
  author={Tan, Xudong and Ye, Peng and Tu, Chongjun and Cao, Jianjian and Yang, Yaoxin and Zhang, Lin and Zhou, Dongzhan and Chen, Tao},
  year={2025},
  eprint={2503.10501},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  doi={10.48550/arXiv.2503.10501},
  url={https://doi.org/10.48550/arXiv.2503.10501},
  note={Version 1, submitted on 13 Mar 2025}
}
```

---

Stay tuned for future updates! 🚀
