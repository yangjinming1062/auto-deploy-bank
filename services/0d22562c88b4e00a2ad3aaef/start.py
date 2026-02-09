#!/usr/bin/env python
"""Startup script that patches Gradio to work with progress tracking without queue."""

import sys

# Patch Gradio's validate_queue_settings to not raise error for progress tracking
import gradio.blocks

original_validate = gradio.blocks.Blocks.validate_queue_settings

def patched_validate(self):
    """Patched validation that allows progress without explicit queue configuration."""
    try:
        # Try original first
        return original_validate(self)
    except ValueError as e:
        if "Progress tracking requires queuing to be enabled" in str(e):
            # For Gradio 3.x, we'll just skip this validation
            pass
        else:
            raise

gradio.blocks.Blocks.validate_queue_settings = patched_validate

# Now import and run the main app
from demo import demo

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)