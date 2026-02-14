from flask import Blueprint, request, jsonify
from ..models import Favorite
from ..utils.auth_utils import serialize_document
from flask_jwt_extended import jwt_required, get_jwt_identity

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('', methods=['GET'])
@jwt_required()
def get_favorites():
    current_user_id = get_jwt_identity()
    favorites = Favorite.get_user_favorites(current_user_id)
    return jsonify([serialize_document(f) for f in favorites]), 200

@favorites_bp.route('', methods=['POST'])
@jwt_required()
def add_favorite():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    city_name = data.get('cityName')
    
    if not city_name:
        return jsonify({'message': 'City name is required'}), 400
        
    fav_id = Favorite.add_favorite(current_user_id, city_name)
    
    if not fav_id:
        return jsonify({'message': 'City already in favorites'}), 400
        
    return jsonify({'id': str(fav_id), 'cityName': city_name, 'msg': 'City added to favorites'}), 201

@favorites_bp.route('/<favorite_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(favorite_id):
    current_user_id = get_jwt_identity()
    success = Favorite.remove_favorite(favorite_id, current_user_id)
    
    if not success:
        return jsonify({'message': 'Favorite not found or not authorized'}), 404
        
    return jsonify({'message': 'Favorite removed'}), 200
