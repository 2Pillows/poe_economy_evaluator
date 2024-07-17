# reforge_influence_routes.py
from flask import Blueprint, jsonify, request
from dataclasses import asdict
from backend.routes.utils import handle_post

from backend.scripts.reforge_influence.influence_main import (
    ReforgeInfluenceData,
    start_influnece_main,
)

reforge_influence_bp = Blueprint("reforge_influence", __name__)


@reforge_influence_bp.route("/api/reforge_influence", methods=["GET"])
def get_reforge_influence():
    start_influnece_main()
    return jsonify(asdict(ReforgeInfluenceData()))


@reforge_influence_bp.route("/api/reforge_influence", methods=["POST"])
def post_reforge_influence():
    return handle_post(request.json, ReforgeInfluenceData(), start_influnece_main)
