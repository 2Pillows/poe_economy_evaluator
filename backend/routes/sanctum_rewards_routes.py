# sanctum_rewards_routes.py
from flask import Blueprint, jsonify, request
from dataclasses import asdict
from backend.routes.utils import handle_post

from backend.src.sanctum_rewards.sanctum_main import (
    SanctumRewardsData,
    start_sanctum_main,
)

sanctum_rewards_bp = Blueprint("sanctum_rewards", __name__)


@sanctum_rewards_bp.route("/api/sanctum_rewards", methods=["GET"])
def get_sanctum_rewards():
    start_sanctum_main()
    return jsonify(asdict(SanctumRewardsData()))


@sanctum_rewards_bp.route("/api/sanctum_rewards", methods=["POST"])
def post_sanctum_rewards():
    return handle_post(request.json, SanctumRewardsData(), start_sanctum_main)
