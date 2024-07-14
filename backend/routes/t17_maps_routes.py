# t17_maps_routes.py
from flask import Blueprint, jsonify, request
from dataclasses import asdict
from backend.routes.utils import handle_post

from backend.scripts.t17_maps.t17_maps_main import T17MapData, start_t17_maps

t17_maps_bp = Blueprint("t17_maps", __name__)


@t17_maps_bp.route("/api/t17_maps", methods=["GET"])
def get_t17_maps():
    start_t17_maps()
    return jsonify(asdict(T17MapData()))


@t17_maps_bp.route("/api/t17_maps", methods=["POST"])
def post_t17_maps():
    return handle_post(request.json, T17MapData(), start_t17_maps)
