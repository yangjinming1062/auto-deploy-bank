from flask import Flask, request, jsonify
from kwaiagents.agent_start import AgentService

app = Flask(__name__)
agent_service = AgentService()


@app.route('/chat', methods=['POST'])
def chat():
    """Agent chat endpoint"""
    input_dict = request.json

    # Ensure required fields
    if 'query' not in input_dict:
        return jsonify({"error": "Missing 'query' field"}), 400

    # Set defaults
    input_dict.setdefault('id', 'default')
    input_dict.setdefault('history', [])
    input_dict.setdefault('llm_name', 'gpt-3.5-turbo')
    input_dict.setdefault('lang', 'en')
    input_dict.setdefault('max_tokens_num', 4096)
    input_dict.setdefault('tool_names', '["auto"]')
    input_dict.setdefault('max_iter_num', 1)
    input_dict.setdefault('agent_name', '')
    input_dict.setdefault('agent_bio', '')
    input_dict.setdefault('agent_instructions', '')
    input_dict.setdefault('external_knowledge', '')

    result = agent_service.chat(input_dict)
    return jsonify(result)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint - service info"""
    return jsonify({
        "service": "kwaiagents",
        "status": "healthy",
        "endpoints": {
            "GET /": "This info",
            "GET /health": "Health check",
            "POST /chat": "Agent chat interface"
        }
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=41382)