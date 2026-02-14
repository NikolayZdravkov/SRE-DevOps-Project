from flask import Blueprint, jsonify

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200


