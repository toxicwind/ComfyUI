import os
import pandas as pd
import concurrent.futures
from safetensors import safe_open

def analyze_files_in_folder(folder, html_output_file):
    # List all .safetensors files in the folder
    files = [file for file in safe_listdir(folder) if file.endswith('.safetensors')]
    print(f"Analyzing {len(files)} files in folder: {folder}")

    # Process files concurrently and gather reports
    with concurrent.futures.ThreadPoolExecutor() as executor:
        reports = list(executor.map(lambda f: generate_report_from_file(folder, f), files))

    # Create DataFrame and export to HTML
    pd.DataFrame(reports, columns=['File', 'Report']).to_html(html_output_file)
    print(f"Analysis saved to {html_output_file}")

def safe_listdir(folder):
    # Function to list files in a directory
    files = [file for file in os.listdir(folder) if file.endswith('.safetensors')]
    print(f"Analyzing {len(files)} files in folder: {folder}")
    return files

def generate_report_from_file(folder, file):
    try:
        # Read file content using safetensors
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with safe_open(file_path, framework='pt') as f:
                content = f.read()  # Read the content from the file correctly
                report = analyze_content(content)
            return file, report
        else:
            raise IOError(f"File {file_path} is not readable")
    except Exception as e:
        print(f"Error in processing {file}: {e}")
        return file, "Error in processing"

def analyze_content(content):
    keys = get_keys()
    values = {key: get_value(content, key) for key in keys}
    return format_report(values)

def get_keys():
    # List of keys to extract
    return ["ss_sd_model_name", "ss_clip_skip", "ss_num_train_images", "ss_tag_frequency",
            "ss_epoch", "ss_face_crop_aug_range", "ss_full_fp16", "ss_gradient_accumulation_steps",
            "ss_gradient_checkpointing", "ss_learning_rate", "ss_lowram", "ss_lr_scheduler",
            "ss_lr_warmup_steps", "ss_max_grad_norm", "ss_max_token_length", "ss_max_train_steps",
            "ss_min_snr_gamma", "ss_mixed_precision", "ss_network_alpha", "ss_network_dim",
            "ss_network_module", "ss_new_sd_model_hash", "ss_noise_offset", "ss_num_batches_per_epoch",
            "ss_cache_latents", "ss_caption_dropout_every_n_epochs", "ss_caption_dropout_rate",
            "ss_caption_tag_dropout_rate", "ss_dataset_dirs", "ss_num_epochs", "ss_num_reg_images",
            "ss_optimizer", "ss_output_name", "ss_prior_loss_weight", "ss_sd_model_hash", "ss_noise_offset", "ss_num_batches_per_epoch", "ss_cache_latents", "ss_caption_dropout_every_n_epochs", "ss_caption_dropout_rate", "ss_caption_tag_dropout_rate", "ss_dataset_dirs", "ss_num_epochs", "ss_num_reg_images", "ss_optimizer", "ss_output_name", "ss_prior_loss_weight", "ss_sd_model_hash", "ss_sd_scripts_commit_hash", "ss_seed", "ss_session_id", "ss_text_encoder_lr", "ss_unet_lr", "ss_v2", "sshs_legacy_hash", "sshs_model_hash"]

def format_report(values):
    # Format the extracted values into a report string
    report_lines = [f"- {key.replace('ss_', '').replace('_', ' ').title()}: {value}" for key, value in values.items()]
    return "Executive Summary Report:\n\n" + "\n".join(report_lines)

def get_value(content, key):
    start = content.find(key) + len(key) + 3  # Add 3 to skip the characters ': ",'
    end = content.find('"', start)
    value = content[start:end]
    return value

folder = 'D:\\sd\\ComfyUI\\models\\checkpoints'
html_output_file = 'analysis_results.html'
analyze_files_in_folder(folder, html_output_file)