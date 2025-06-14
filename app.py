from flask import Flask, request, jsonify
from flask_cors import CORS
from assistant import ConversationAssistant
import logging
import time

app = Flask(__name__)
CORS(app)

# Configure logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

assistant = ConversationAssistant()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '')
        source = data.get('source', 'auto')
        target = data.get('target', 'en')
        
        if not text:
            return jsonify({'success': False, 'error': 'Please enter text to translate'}), 400
            
        translated = assistant.translate_text(text, source, target)
        return jsonify({'success': True, 'translation': translated})
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Translation service unavailable',
            'solution': 'Try again later or check your internet connection'
        }), 503

@app.route('/translate-multi', methods=['POST'])
def translate_multi():
    start_time = time.time()
    try:
        data = request.json
        text = data.get('text', '')
        source = data.get('source', 'auto')
        targets = data.get('targets', ['en'])

        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        if not isinstance(targets, list):
            return jsonify({'success': False, 'error': 'Invalid targets format'}), 400

        results = {}
        for lang in targets:
            try:
                translated = assistant.translate_text(text, source, lang)
                results[lang] = translated
            except Exception as e:
                results[lang] = f'Translation failed: {str(e)}'

        logger.info(f"Multi-translation completed in {time.time() - start_time:.2f}s")
        return jsonify({'success': True, 'translations': results})
        
    except Exception as e:
        logger.error(f"Multi-translation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Translation service unavailable',
            'details': str(e)
        }), 503

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)