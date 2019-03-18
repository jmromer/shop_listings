import os

from flask import Flask, jsonify, make_response, request, send_from_directory
from flask_cors import CORS
from flask_redis import FlaskRedis

from services.etsy_find_all_shops import get_shops_list
from services.shop_listings_analysis import perform_analysis

app = Flask(__name__, static_folder='build/static', template_folder='build')
app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.config['PORT'] = os.getenv('PORT') or 5000
app.debug = os.getenv('DEBUG') == 'true'

CORS(app)

redis_store = FlaskRedis(app)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ETSY_API_KEY = os.getenv('ETSY_API_KEY', '')
MAX_NUMBER_OF_TERMS = int(os.getenv('MAX_NUMBER_OF_TERMS', '5'))

BUILD_DIR = os.path.join(os.path.abspath(os.path.dirname('.')), 'build')
STATIC_FILES_DIR = f'{BUILD_DIR}/static'


@app.route('/static/<path>/<filename>', methods=['GET'])
def assets(path, filename):
    return send_from_directory(f'{STATIC_FILES_DIR}/{path}', filename)


@app.route('/', methods=['GET'])
def index():
    """Render the Etsy shop selection form."""
    return send_from_directory(BUILD_DIR, 'index.html')


@app.route('/shop-names', methods=['GET'])
def shop_names():
    shop_names = get_shops_list(
        etsy_api_key=ETSY_API_KEY,
        max_stores=50,
        redis_store=redis_store,
        page=1)

    listing = [{'label': name, 'value': name} for name in shop_names]

    return jsonify({'listing': listing})


@app.route('/key-terms', methods=['GET'])
def key_terms():
    """
    Source listings and return meaningful terms for the given `shop_name`,
    perform the analysis if necessary, returning cached values if available.
    """
    shop_names = request.args.get('q')
    if not shop_names:
        resp = jsonify({'error': 'missing query string'})
        return make_response(resp, 422)

    results = []
    for shop_name in shop_names.split(','):
        result = perform_analysis(
            shop_name,
            logger=app.logger,
            log_level=LOG_LEVEL,
            etsy_api_key=ETSY_API_KEY,
            max_number_of_terms=MAX_NUMBER_OF_TERMS,
            redis_store=redis_store)
        results.append(result)

    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)
