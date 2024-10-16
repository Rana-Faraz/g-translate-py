from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def translate_nested(data, src_language, dest_languages):
    translations = {src_language: data}
    for dest_language in dest_languages:
        translations[dest_language] = {}

    def recursive_translate(src_obj, dest_objs, src_language, dest_languages):
        app.logger.debug(f"Translating: {src_obj}")
        for key, value in src_obj.items():
            if isinstance(value, dict):
                for lang in dest_languages:
                    dest_objs[lang][key] = {}
                recursive_translate(value, {lang: dest_objs[lang][key] for lang in dest_languages}, src_language, dest_languages)
            else:
                for lang in dest_languages:
                    translator = GoogleTranslator(source=src_language, target=lang)
                    translated_text = translator.translate(value)
                    dest_objs[lang][key] = translated_text

    recursive_translate(data, {lang: translations[lang] for lang in dest_languages}, src_language, dest_languages)
    return translations

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        app.logger.debug(f"Received data: {data}")
        
        if not data:
            return jsonify({'error': 'Request payload is missing'}), 400

        if len(data.keys()) == 0:
            return jsonify({'error': 'Source language key is missing'}), 400

        src_language = list(data.keys())[0]
        app.logger.debug(f"Source language: {src_language}")

        if not isinstance(data[src_language], dict) or 'translation' not in data[src_language]:
            return jsonify({'error': 'Translation data is missing or not properly formatted'}), 400

        translations_dict = data[src_language]['translation']
        if not isinstance(translations_dict, dict):
            return jsonify({'error': 'Translations must be an object'}), 400
        
        app.logger.debug(f"Translations dict: {translations_dict}")
        
        # Hard-code destination languages
        dest_languages = ["ar"]
        app.logger.debug(f"Hard-coded destination languages: {dest_languages}")
        
        result = translate_nested(translations_dict, src_language, dest_languages)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
