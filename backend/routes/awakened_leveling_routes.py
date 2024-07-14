# awakened_leveling_routes.py
from flask import Blueprint, jsonify, request
from dataclasses import asdict
from backend.routes.utils import handle_post

from backend.scripts.awakened_leveling.awakened_main import (
    AwakenedLevelingData,
    start_awakened_main,
)


awakened_leveling_bp = Blueprint("awakened_leveling", __name__)


@awakened_leveling_bp.route("/api/awakened_leveling", methods=["GET"])
def get_awakened_leveling():
    start_awakened_main()
    return jsonify(asdict(AwakenedLevelingData()))


@awakened_leveling_bp.route("/api/awakened_leveling", methods=["POST"])
def post_awakened_leveling():
    return handle_post(request.json, AwakenedLevelingData(), start_awakened_main)
