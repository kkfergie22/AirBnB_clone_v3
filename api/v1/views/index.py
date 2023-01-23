from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status')
def status():
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def stats():
    if request.method == 'GET':
        return jsonify(storage.count())
