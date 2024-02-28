import torch

from palm_rlhf_pytorch import PaLM

model = PaLM(
    num_tokens=50304, dim=1024, depth=24, dim_head=128, heads=8, flash_attn=True, qk_rmsnorm = False,
).cuda()

model.load('/palm_410m_8k_v0.pt')
