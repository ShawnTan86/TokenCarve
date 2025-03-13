# TokenCarve: Information-Preserving Visual Token Compression in Multimodal Large Language Models

## News

🌟 **[2025/3/13]** Our work is now available on [arXiv](https://arxiv.org/auth/need-endorsement.php?tapir_dest=https%3A%2F%2Farxiv.org%2Fsubmit%2F6276999%2Fstart&category_id=cs.CV)!

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

## Contents

- [News](#news)
- [Overview](#overview)
- [Contents](#contents)
- [Usage](#usage)
- [Citation](#citation)

---

## Usage

Our code is currently being organized and will be released soon.

---

## Citation

If you use our code for your paper, please cite:

```bibtex
@ARTICLE{10158936,
  author={Tan, Xudong and Hu, Menghan and Zhai, Guangtao and Zhu, Yan and Li, Wenfang and Zhang, Xiao-Ping},
  journal={IEEE Transactions on Multimedia}, 
  title={Lightweight Video-Based Respiration Rate Detection Algorithm: An Application Case on Intensive Care}, 
  year={2023},
  volume={},
  number={},
  pages={1-15},
  doi={10.1109/TMM.2023.3286994}
}
```

---

Stay tuned for future updates! 🚀
