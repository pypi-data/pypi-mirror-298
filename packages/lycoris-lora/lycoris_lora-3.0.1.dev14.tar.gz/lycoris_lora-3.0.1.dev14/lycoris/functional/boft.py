import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from einops import rearrange

from .general import power2factorization, FUNC_LIST
from .diag_oft import get_r


def weight_gen(org_weight, max_block_size, boft_m=-1, rescale=False):
    """### boft_weight_gen

    Args:
        org_weight (torch.Tensor): the weight tensor
        max_block_size (int): max block size
        rescale (bool, optional): whether to rescale the weight. Defaults to False.

    Returns:
        torch.Tensor: oft_blocks[, rescale_weight]
    """
    out_dim, *rest = org_weight.shape
    block_size, block_num = power2factorization(out_dim, max_block_size)
    max_boft_m = sum(int(i) for i in f"{block_num-1:b}") + 1
    if boft_m == -1:
        boft_m = max_boft_m
    boft_m = min(boft_m, max_boft_m)
    oft_blocks = torch.zeros(boft_m, block_num, block_size, block_size)
    if rescale is not None:
        return oft_blocks, torch.ones(out_dim, *[1] * len(rest))
    else:
        return oft_blocks, None


def diff_weight(org_weight, oft_blocks, rescale=None, constraint=None):
    """### boft_diff_weight

    Args:
        TODO

    Returns:
        torch.Tensor: ΔW
    """
    m, num, b, _ = oft_blocks.shape
    r_b = b // 2
    I = torch.eye(b, device=oft_blocks.device)
    r = get_r(oft_blocks, I, constraint)
    inp = org = org_weight.to(dtype=r.dtype)

    for i in range(m):
        bi = r[i]  # b_num, b_size, b_size
        inp = rearrange(inp, "(c g k) ... -> (c k g) ...", g=2, k=2**i * r_b)
        inp = rearrange(inp, "(d b) ... -> d b ...", b=b)
        inp = torch.einsum("b i j, b j ... -> b i ...", bi, inp)
        inp = rearrange(inp, "d b ... -> (d b) ...")
        inp = rearrange(inp, "(c k g) ... -> (c g k) ...", g=2, k=2**i * r_b)

    if rescale is not None:
        inp = inp * rescale

    return inp - org


def bypass_forward_diff(
    org_out, oft_blocks, rescale=None, constraint=None, need_transpose=False
):
    """### boft_bypass_forward_diff

    Args:
        TODO

    Returns:
        torch.Tensor: output tensor
    """
    m, num, b, _ = oft_blocks.shape
    r_b = b // 2
    I = torch.eye(b, device=oft_blocks.device)
    r = get_r(oft_blocks, I, constraint)
    inp = org = org_out.to(dtype=r.dtype)
    if need_transpose:
        inp = org = inp.transpose(1, -1)

    for i in range(m):
        bi = r[i]  # b_num, b_size, b_size
        inp = rearrange(inp, "... (c g k) ->... (c k g)", g=2, k=2**i * r_b)
        inp = rearrange(inp, "... (d b) -> ... d b", b=b)
        inp = torch.einsum("b i j, ... b j -> ... b i", bi, inp)
        inp = rearrange(inp, "... d b -> ... (d b)")
        inp = rearrange(inp, "... (c k g) -> ... (c g k)", g=2, k=2**i * r_b)

    if rescale is not None:
        inp = inp * rescale.transpose(0, -1)

    inp = inp - org
    if need_transpose:
        inp = inp.transpose(1, -1)
    return inp
