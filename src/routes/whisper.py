import os
import tempfile
import whisper
import torch
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

whisper_bp = Blueprint('whisper', __name__)

# Global variable to store the loaded model
loaded_model = None
current_model_name = None

def get_device():
    """Determine the best device to use (CUDA if available, otherwise CPU)"""
    if torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"

def load_whisper_model(model_name="base"):
    """Load Whisper model with caching"""
    global loaded_model, current_model_name
    
    if loaded_model is None or current_model_name != model_name:
        logger.info(f"Loading Whisper model: {model_name}")
        device = get_device()
        logger.info(f"Using device: {device}")
        
        try:
            loaded_model = whisper.load_model(model_name, device=device)
            current_model_name = model_name
            logger.info(f"Model {model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {str(e)}")
            raise
    
    return loaded_model

def validate_api_key(request):
    """Validate API key from request headers"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False, "Missing Authorization header"
    
    if not auth_header.startswith('Bearer '):
        return False, "Invalid Authorization header format"
    
    api_key = auth_header[7:]  # Remove 'Bearer ' prefix
    
    # For now, accept any non-empty API key
    # In production, you should validate against a database or environment variable
    if not api_key:
        return False, "Empty API key"
    
    return True, "Valid API key"

@whisper_bp.route('/audio/transcriptions', methods=['POST'])
def transcribe_audio():
    """OpenAI-compatible transcription endpoint"""
    try:
        # Validate API key
        is_valid, message = validate_api_key(request)
        if not is_valid:
            return jsonify({"error": {"message": message, "type": "authentication_error"}}), 401
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": {"message": "No file provided", "type": "invalid_request_error"}}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": {"message": "No file selected", "type": "invalid_request_error"}}), 400
        
        # Get parameters
        model_name = request.form.get('model', 'whisper-1')
        language = request.form.get('language', None)
        prompt = request.form.get('prompt', None)
        response_format = request.form.get('response_format', 'json')
        temperature = float(request.form.get('temperature', 0.0))
        
        # Map OpenAI model names to Whisper model names
        model_mapping = {
            'whisper-1': 'base',
            'whisper-large': 'large',
            'whisper-medium': 'medium',
            'whisper-small': 'small',
            'whisper-tiny': 'tiny'
        }
        
        actual_model = model_mapping.get(model_name, 'base')
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Load model
            model = load_whisper_model(actual_model)
            
            # Transcribe audio
            options = {
                "temperature": temperature,
                "task": "transcribe"
            }
            
            if language:
                options["language"] = language
            
            if prompt:
                options["initial_prompt"] = prompt
            
            result = model.transcribe(temp_file_path, **options)
            
            # Format response based on requested format
            if response_format == 'text':
                return result["text"]
            elif response_format == 'verbose_json':
                return jsonify({
                    "task": "transcribe",
                    "language": result.get("language", "unknown"),
                    "duration": result.get("duration", 0),
                    "text": result["text"],
                    "segments": result.get("segments", [])
                })
            else:  # json (default)
                return jsonify({
                    "text": result["text"]
                })
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except Exception as e:
        logger.error(f"Error in transcription: {str(e)}")
        return jsonify({"error": {"message": str(e), "type": "server_error"}}), 500

@whisper_bp.route('/audio/translations', methods=['POST'])
def translate_audio():
    """OpenAI-compatible translation endpoint"""
    try:
        # Validate API key
        is_valid, message = validate_api_key(request)
        if not is_valid:
            return jsonify({"error": {"message": message, "type": "authentication_error"}}), 401
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": {"message": "No file provided", "type": "invalid_request_error"}}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": {"message": "No file selected", "type": "invalid_request_error"}}), 400
        
        # Get parameters
        model_name = request.form.get('model', 'whisper-1')
        prompt = request.form.get('prompt', None)
        response_format = request.form.get('response_format', 'json')
        temperature = float(request.form.get('temperature', 0.0))
        
        # Map OpenAI model names to Whisper model names
        model_mapping = {
            'whisper-1': 'base',
            'whisper-large': 'large',
            'whisper-medium': 'medium',
            'whisper-small': 'small',
            'whisper-tiny': 'tiny'
        }
        
        actual_model = model_mapping.get(model_name, 'base')
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Load model
            model = load_whisper_model(actual_model)
            
            # Translate audio (always to English)
            options = {
                "temperature": temperature,
                "task": "translate"
            }
            
            if prompt:
                options["initial_prompt"] = prompt
            
            result = model.transcribe(temp_file_path, **options)
            
            # Format response based on requested format
            if response_format == 'text':
                return result["text"]
            elif response_format == 'verbose_json':
                return jsonify({
                    "task": "translate",
                    "language": result.get("language", "unknown"),
                    "duration": result.get("duration", 0),
                    "text": result["text"],
                    "segments": result.get("segments", [])
                })
            else:  # json (default)
                return jsonify({
                    "text": result["text"]
                })
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except Exception as e:
        logger.error(f"Error in translation: {str(e)}")
        return jsonify({"error": {"message": str(e), "type": "server_error"}}), 500

@whisper_bp.route('/models', methods=['GET'])
def list_models():
    """List available models (OpenAI-compatible)"""
    is_valid, message = validate_api_key(request)
    if not is_valid:
        return jsonify({"error": {"message": message, "type": "authentication_error"}}), 401
    
    models = [
        {
            "id": "whisper-1",
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai-internal"
        }
    ]
    
    return jsonify({
        "object": "list",
        "data": models
    })

