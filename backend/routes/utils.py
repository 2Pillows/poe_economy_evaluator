from flask import jsonify
from dataclasses import asdict

from backend.src.api_data import API_Data


def handle_post(request_data, class_data, start_function):
    api_data = API_Data()
    if request_data:
        for key, value in request_data.items():
            if hasattr(api_data, key):
                setattr(api_data, key, value)
            elif hasattr(class_data, key):
                setattr(class_data, key, value)

        start_function()

        return jsonify(asdict(class_data))
    else:
        return jsonify({"error": "No data provided in the request"}), 400
