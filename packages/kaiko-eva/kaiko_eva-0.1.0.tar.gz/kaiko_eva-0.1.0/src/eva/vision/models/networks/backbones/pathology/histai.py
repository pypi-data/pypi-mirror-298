"""Pathology FMs from owkin."""

from typing import Tuple

from torch import nn

from eva.vision.models.networks.backbones import _utils
from eva.vision.models.networks.backbones.registry import register_model


@register_model("pathology/histai_hibou_b")
def histai_hibou_b(out_indices: int | Tuple[int, ...] | None = None) -> nn.Module:
    """Initializes the hibou-B pathology FM by hist.ai (https://huggingface.co/histai/hibou-B).

    Args:
        out_indices: Whether and which multi-level patch embeddings to return.
            Currently only out_indices=1 is supported.

    Returns:
        The model instance.
    """
    return _utils.load_hugingface_model(
        model_name="histai/hibou-B",
        out_indices=out_indices,
        model_kwargs={"trust_remote_code": True},
        transform_args={"ignore_remaining_dims": True} if out_indices is not None else None,
    )


@register_model("pathology/histai_hibou_l")
def histai_hibou_l(out_indices: int | Tuple[int, ...] | None = None) -> nn.Module:
    """Initializes the hibou-L pathology FM by hist.ai (https://huggingface.co/histai/hibou-L).

    Args:
        out_indices: Whether and which multi-level patch embeddings to return.
            Currently only out_indices=1 is supported.

    Returns:
        The model instance.
    """
    return _utils.load_hugingface_model(
        model_name="histai/hibou-L",
        out_indices=out_indices,
        model_kwargs={"trust_remote_code": True},
        transform_args={"ignore_remaining_dims": True} if out_indices is not None else None,
    )
