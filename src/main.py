import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS
from src.routes.whisper import whisper_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whisper-api-secret-key-2025'

# Enable CORS for all routes
CORS(app)

# Register Whisper API blueprint
app.register_blueprint(whisper_bp, url_prefix='/v1')

@app.route('/')
def health_check():
    return {"status": "ok", "message": "Whisper API is running"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9005, debug=True)
