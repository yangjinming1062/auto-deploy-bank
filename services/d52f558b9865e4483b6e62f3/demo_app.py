"""
Demo Gradio app for LLamaTuner Docker deployment.
This provides a minimal UI that shows the service is running.
"""
import gradio as gr


def chat_response(message, history):
    """Simple echo response for demo purposes."""
    return f"Demo mode: You said '{message}'. Configure MODEL_NAME_OR_PATH to enable LLM responses."


with gr.Blocks(title="LLamaTuner Demo") as demo:
    gr.Markdown("# LLamaTuner - LLM Fine-Tuning Web UI")
    gr.Markdown("**Demo Mode** - Configure `MODEL_NAME_OR_PATH` environment variable with a HuggingFace model path to enable full functionality.")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Enter your message", placeholder="Type here...")
    clear = gr.Button("Clear")

    def respond(message, history):
        response = chat_response(message, history)
        history.append((message, response))
        return "", history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: (None, None), outputs=[msg, chatbot])

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860)