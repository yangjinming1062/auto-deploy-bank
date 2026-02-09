from flask import Flask, request, jsonify, render_template_string
from tensorflow.keras.models import load_model
from kapre.time_frequency import STFT, Magnitude, ApplyFilterbank, MagnitudeToDecibel
from clean import downsample_mono, envelope
import numpy as np
import os
import tempfile

app = Flask(__name__)

# Model configuration
MODEL_PATH = os.environ.get('MODEL_PATH', 'models/lstm.h5')
SAMPLE_RATE = 16000
DELTA_TIME = 1.0
THRESHOLD = 20

# Class labels (based on folder structure)
CLASSES = ['Acoustic_guitar', 'Bass_drum', 'Cello', 'Clarinet', 'Double_bass',
           'Drums', 'Flute', 'Guitar', 'Harmonica', 'Piano']

# Load model once at startup
model = None

def load_model_once():
    global model
    if model is None:
        try:
            model = load_model(MODEL_PATH,
                custom_objects={
                    'STFT': STFT,
                    'Magnitude': Magnitude,
                    'ApplyFilterbank': ApplyFilterbank,
                    'MagnitudeToDecibel': MagnitudeToDecibel
                })
            print(f"Model loaded successfully from {MODEL_PATH}")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Try to find any existing model
            for root, dirs, files in os.walk('models'):
                for f in files:
                    if f.endswith('.h5'):
                        try:
                            model = load_model(os.path.join(root, f),
                                custom_objects={
                                    'STFT': STFT,
                                    'Magnitude': Magnitude,
                                    'ApplyFilterbank': ApplyFilterbank,
                                    'MagnitudeToDecibel': MagnitudeToDecibel
                                })
                            print(f"Loaded model: {os.path.join(root, f)}")
                            return
                        except:
                            continue

def predict_audio(wav_path):
    """Predict the class of an audio file."""
    if model is None:
        load_model_once()
    if model is None:
        return None, "Model not loaded"

    try:
        rate, wav = downsample_mono(wav_path, SAMPLE_RATE)
        mask, env = envelope(wav, rate, threshold=THRESHOLD)
        clean_wav = wav[mask]

        step = int(SAMPLE_RATE * DELTA_TIME)
        batch = []

        for i in range(0, clean_wav.shape[0], step):
            sample = clean_wav[i:i+step]
            sample = sample.reshape(-1, 1)
            if sample.shape[0] < step:
                tmp = np.zeros(shape=(step, 1), dtype=np.float32)
                tmp[:sample.shape[0], :] = sample.flatten().reshape(-1, 1)
                sample = tmp
            batch.append(sample)

        X_batch = np.array(batch, dtype=np.float32)
        y_pred = model.predict(X_batch)
        y_mean = np.mean(y_pred, axis=0)
        y_pred_idx = np.argmax(y_mean)

        return {
            'predicted_class': CLASSES[y_pred_idx] if y_pred_idx < len(CLASSES) else 'Unknown',
            'confidence': float(np.max(y_mean)),
            'probabilities': {CLASSES[i]: float(y_mean[i]) for i in range(len(CLASSES))}
        }, None
    except Exception as e:
        return None, str(e)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Audio Classification Service</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .upload-form { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
        input[type="file"] { margin: 10px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        #result { margin-top: 20px; padding: 15px; border-radius: 4px; display: none; }
        .success { background: #d4edda; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; border: 1px solid #f5c6cb; }
        .prediction { font-size: 1.2em; font-weight: bold; }
        .confidence { color: #666; }
        .prob-list { margin-top: 10px; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>Audio Classification Service</h1>
    <p>Upload an audio file to classify its instrument type.</p>
    <div class="upload-form">
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="audio" accept=".wav,.mp3" required>
            <button type="submit">Classify Audio</button>
        </form>
    </div>
    <div id="result"></div>
    <script>
        document.querySelector('form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.className = '';
            resultDiv.innerHTML = 'Processing...';
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.error) {
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = 'Error: ' + data.error;
                } else {
                    resultDiv.className = 'success';
                    resultDiv.innerHTML = `
                        <p class="prediction">Predicted: ${data.predicted_class}</p>
                        <p class="confidence">Confidence: ${(data.confidence * 100).toFixed(2)}%</p>
                        <div class="prob-list">
                            <strong>All Probabilities:</strong>
                            <ul>
                                ${Object.entries(data.probabilities).map(([k, v]) =>
                                    `<li>${k}: ${(v * 100).toFixed(2)}%</li>`).join('')}
                            </ul>
                        </div>
                    `;
                }
            } catch (err) {
                resultDiv.className = 'error';
                resultDiv.innerHTML = 'Error: ' + err.message;
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result, error = predict_audio(tmp_path)
        if error:
            return jsonify({'error': error}), 500
        return jsonify(result)
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    load_model_once()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)