from flask import Flask

app = Flask(__name__)


@app.route('/')
def health():
    return 'Qlib service is running', 200


@app.route('/health')
def health_check():
    return {'status': 'healthy', 'service': 'qlib'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=42550)