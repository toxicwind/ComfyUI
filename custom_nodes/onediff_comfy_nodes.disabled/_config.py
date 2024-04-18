"""Config file for comfyui-speedup, which will automatically"""
import os
import sys
from pathlib import Path

ONEDIFF_QUANTIZED_OPTIMIZED_MODELS = "onediff_quant"
_USE_UNET_INT8 = True
COMFYUI_ROOT = Path(os.path.abspath(__file__)).parents[2]
COMFYUI_SPEEDUP_ROOT = Path(os.path.abspath(__file__)).parents[0]
INFER_COMPILER_REGISTRY = Path(COMFYUI_SPEEDUP_ROOT) / "infer_compiler_registry"

sys.path.insert(0, str(COMFYUI_ROOT))
sys.path.insert(0, str(COMFYUI_SPEEDUP_ROOT))
sys.path.insert(0, str(INFER_COMPILER_REGISTRY))
import register_comfy  # load plugins
from onediff.infer_compiler.utils import is_community_version

if is_community_version():
    _USE_UNET_INT8 = False

if _USE_UNET_INT8:
    import register_onediff_quant  # load plugins

    from folder_paths import folder_names_and_paths, supported_pt_extensions, models_dir

    unet_int8_model_dir = Path(models_dir) / "unet_int8"
    unet_int8_model_dir.mkdir(parents=True, exist_ok=True)
    folder_names_and_paths["unet_int8"] = (
        [str(unet_int8_model_dir)],
        supported_pt_extensions,
    )

    opt_models_dir = Path(models_dir) / ONEDIFF_QUANTIZED_OPTIMIZED_MODELS
    opt_models_dir.mkdir(parents=True, exist_ok=True)

    folder_names_and_paths[ONEDIFF_QUANTIZED_OPTIMIZED_MODELS] = (
        [str(opt_models_dir)],
        supported_pt_extensions,
    )
