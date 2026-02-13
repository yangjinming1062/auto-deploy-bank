"""Flask web service wrapper for markitdown CLI tool."""
import os
import tempfile
from flask import Flask, request, send_file, Response
from markitdown import MarkItDown

app = Flask(__name__)

# Initialize MarkItDown
md = MarkItDown()


@app.route('/convert', methods=['POST'])
def convert_file():
    """Convert uploaded file to markdown."""
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400

    file = request.files['file']

    if file.filename == '':
        return {'error': 'No file selected'}, 400

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Convert to markdown
        result = md.convert(tmp_path)
        return {'markdown': result.text_content}
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        # Cleanup temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.route('/', methods=['GET'])
def index():
    """Root endpoint - service info."""
    return {
        'service': 'markitdown-api',
        'status': 'running',
        'endpoints': {
            '/': 'GET - This info',
            '/health': 'GET - Health check',
            '/convert': 'POST - Convert file to markdown'
        }
    }, 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return {'status': 'ok'}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)