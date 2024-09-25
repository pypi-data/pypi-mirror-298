import functools
import importlib
import os

import torch

from .quant_api import apply_fp8_dynamic_quant, apply_int8_dynamic_quant

from .quant_module import Fp8QuantLinear, Int8QuantLinear, QuantModuleBase

NEXFORT_QUANT_TYPE = os.environ.get("NEXFORT_QUANT_TYPE", "int8_dynamic")


def quantize(module, *, quant_type=NEXFORT_QUANT_TYPE, filter_fn=None, filter_fn_kwargs=None):
    supported_quant_types = (
        "int8_dynamic",
        "fp8_e4m3_e4m3_dynamic",
        "fp8_e5m2_e5m2_dynamic",
        "fp8_e4m3_e4m3_dynamic_per_tensor",
        "fp8_e5m2_e5m2_dynamic_per_tensor",
    )
    assert quant_type in supported_quant_types, f"Unsupported quant_type: {quant_type}"

    if isinstance(filter_fn, str):
        if "." in filter_fn:
            module_name, attr_name = filter_fn.rsplit(".", 1)
        else:
            module_name, attr_name = "nexfort.quantization.filter_functions", filter_fn
        filter_fn = getattr(importlib.import_module(module_name), attr_name)
    if filter_fn is not None and filter_fn_kwargs is not None:
        filter_fn = functools.partial(filter_fn, **filter_fn_kwargs)

    if quant_type == "int8_dynamic":
        apply_int8_dynamic_quant(
            module, filter_fn=filter_fn, symm_quant_act=True, act_per_tensor=False, weight_per_tensor=False
        )
    elif quant_type == "fp8_e4m3_e4m3_dynamic":
        apply_fp8_dynamic_quant(
            module, fp8_dtype=torch.float8_e4m3fn, filter_fn=filter_fn, act_per_tensor=False, weight_per_tensor=False
        )
    elif quant_type == "fp8_e5m2_e5m2_dynamic":
        apply_fp8_dynamic_quant(
            module, fp8_dtype=torch.float8_e5m2, filter_fn=filter_fn, act_per_tensor=False, weight_per_tensor=False
        )
    elif quant_type == "fp8_e4m3_e4m3_dynamic_per_tensor":
        apply_fp8_dynamic_quant(
            module, fp8_dtype=torch.float8_e4m3fn, filter_fn=filter_fn, act_per_tensor=False, weight_per_tensor=True
        )
    elif quant_type == "fp8_e5m2_e5m2_dynamic_per_tensor":
        apply_fp8_dynamic_quant(
            module, fp8_dtype=torch.float8_e5m2, filter_fn=filter_fn, act_per_tensor=False, weight_per_tensor=True
        )
    else:
        raise ValueError(f"Unsupported quant_type: {quant_type}")
    return module


def is_quantized_module(module, *, quant_type=None):
    if quant_type is None:
        choices = QuantModuleBase
    elif quant_type == "int8_dynamic":
        choices = Int8QuantLinear
    elif quant_type in (
        "fp8_e4m3_e4m3_dynamic",
        "fp8_e5m2_e5m2_dynamic",
        "fp8_e4m3_e4m3_dynamic_per_tensor",
        "fp8_e5m2_e5m2_dynamic_per_tensor",
    ):
        choices = Fp8QuantLinear
    else:
        raise ValueError(f"Unsupported quant_type: {quant_type}")
    for name, child in model.named_children():
        if isinstance(child, choices):
            return True
    return False
