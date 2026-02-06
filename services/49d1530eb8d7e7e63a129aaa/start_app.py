#!/usr/bin/env python
"""
DMD2-SDXL Demo Server

This is a simple Gradio server for the DMD2-SDXL model.
It provides a web interface for text-to-image generation.

Usage:
    python start_app.py [--host HOST] [--port PORT] [--checkpoint_path PATH]

Environment Variables:
    CHECKPOINT_PATH: Path to the model checkpoint (optional)
    CUDA_VISIBLE_DEVICES: GPU device ID (default: 0)
"""

import gradio as gr
import argparse
import os
import sys

# Global model wrapper - loaded lazily
model_wrapper = None

def create_demo_with_checkpoint(checkpoint_path):
    """Create the demo with a given checkpoint path."""
    global model_wrapper

    # Import here to avoid loading heavy deps if not needed
    from demo.text_to_image_sdxl import ModelWrapper, create_demo
    from accelerate import Accelerator
    import argparse

    # Parse arguments similar to the original demo
    parser = argparse.ArgumentParser()
    parser.add_argument("--latent_resolution", type=int, default=128)
    parser.add_argument("--image_resolution", type=int, default=1024)
    parser.add_argument("--num_train_timesteps", type=int, default=1000)
    parser.add_argument("--checkpoint_path", type=str, default=checkpoint_path)
    parser.add_argument("--model_id", type=str, default="stabilityai/stable-diffusion-xl-base-1.0")
    parser.add_argument("--precision", type=str, default="float32", choices=["float32", "float16", "bfloat16"])
    parser.add_argument("--conditioning_timestep", type=int, default=999)
    parser.add_argument("--num_step", type=int, default=4, choices=[1, 4])
    parser.add_argument("--revision", type=str)
    args = parser.parse_args([])

    accelerator = Accelerator()
    model_wrapper = ModelWrapper(args, accelerator)

    return create_demo()


def create_placeholder_demo(checkpoint_path=None):
    """Create a placeholder demo when no checkpoint is available."""
    with gr.Blocks(title="DMD2-SDXL Demo") as demo:
        gr.Markdown("# DMD2-SDXL Demo")
        gr.Markdown("## Model Checkpoint Required")
        gr.Markdown("""
        This demo requires a trained model checkpoint to run.

        To provide a checkpoint, either:
        1. Set the CHECKPOINT_PATH environment variable
        2. Pass --checkpoint_path as a command line argument
        3. Mount a checkpoint file and specify the path

        Example:
        ```bash
        python start_app.py --checkpoint_path /path/to/checkpoint
        ```

        Or with docker:
        ```bash
        CHECKPOINT_PATH=/path/to/checkpoint python start_app.py
        ```
        """)

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Current Configuration")
                checkpoint_display = gr.Textbox(
                    value=checkpoint_path or "Not specified",
                    label="Checkpoint Path",
                    interactive=False
                )

    return demo


def main():
    parser = argparse.ArgumentParser(description="DMD2-SDXL Demo Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=7860, help="Port to bind to")
    parser.add_argument("--checkpoint_path", type=str, default=None,
                        help="Path to model checkpoint")
    parser.add_argument("--share", action="store_true", default=False,
                        help="Create public link")

    args = parser.parse_args()

    # Check environment variable if checkpoint not provided
    checkpoint_path = args.checkpoint_path or os.environ.get("CHECKPOINT_PATH")

    if checkpoint_path:
        print(f"Loading model from checkpoint: {checkpoint_path}")
        try:
            demo = create_demo_with_checkpoint(checkpoint_path)
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            print("Falling back to placeholder demo...")
            demo = create_placeholder_demo(checkpoint_path)
    else:
        print("No checkpoint path provided. Starting in placeholder mode.")
        print("Use --checkpoint_path or CHECKPOINT_PATH env var to load a model.")
        demo = create_placeholder_demo()

    demo.queue()
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        show_error=True
    )


if __name__ == "__main__":
    main()