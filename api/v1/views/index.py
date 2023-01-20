from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    return jsonify(storage.count())
