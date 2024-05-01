# six_linking_routes.py
from flask import Blueprint, jsonify, request
from dataclasses import asdict
from backend.routes.utils import handle_post

from backend.src.six_linking.six_linking_main import (
    SixLinkingData,
    start_six_linking_main,
)

six_linking_bp = Blueprint("six_linking", __name__)


@six_linking_bp.route("/api/six_linking", methods=["GET"])
def get_six_linking():
    start_six_linking_main()
    return jsonify(asdict(SixLinkingData()))


@six_linking_bp.route("/api/six_linking", methods=["POST"])
def post_six_linking():
    return handle_post(request.json, SixLinkingData(), start_six_linking_main)
