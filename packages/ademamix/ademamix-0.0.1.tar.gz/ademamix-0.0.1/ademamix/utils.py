import torch


def _get_scalar_dtype(is_fused=None):
    if is_fused:
        return torch.float32
    return (
        torch.float64 if torch.get_default_dtype() == torch.float64 else torch.float32
    )


def _get_value(x):
    if not torch.jit.is_scripting() and torch.compiler.is_compiling():
        return x
    else:
        return x.item() if isinstance(x, torch.Tensor) else x
