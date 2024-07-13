# chaos_res_crafting_routes.py
from flask import Blueprint, jsonify, request
from dataclasses import asdict
from backend.routes.utils import handle_post

from backend.src.chaos_res_crafting.chaos_res_crafting_main import (
    ChaosResCraftingData,
    start_chaos_res_crafting,
)


chaos_res_crafting_bp = Blueprint("chaos_res_crafting", __name__)


@chaos_res_crafting_bp.route("/api/chaos_res_crafting", methods=["GET"])
def get_chaos_res_crafting():
    start_chaos_res_crafting()
    return jsonify(asdict(ChaosResCraftingData()))


@chaos_res_crafting_bp.route("/api/chaos_res_crafting", methods=["POST"])
def post_chaos_res_crafting():
    return handle_post(request.json, ChaosResCraftingData(), start_chaos_res_crafting)
