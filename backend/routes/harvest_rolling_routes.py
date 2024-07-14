# Harvest_Rolling_routes.py
from flask import Blueprint, jsonify, request
from dataclasses import asdict
from backend.routes.utils import handle_post

from backend.scripts.harvest_rolling.harvest_main import (
    HarvestRollingData,
    start_harvest_main,
)

harvest_rolling_bp = Blueprint("harvest_rolling", __name__)


@harvest_rolling_bp.route("/api/harvest_rolling", methods=["GET"])
def get_harvest_rolling():
    start_harvest_main()
    return jsonify(asdict(HarvestRollingData()))


@harvest_rolling_bp.route("/api/harvest_rolling", methods=["POST"])
def post_harvest_rolling():
    return handle_post(request.json, HarvestRollingData(), start_harvest_main)
