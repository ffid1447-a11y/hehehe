from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TARGET_URL = "https://offlinechallanapi-3yh6els5ia-uc.a.run.app/vehicle/mobile-no"

def fetch_mobile(reg_number):
    payload = {"reg_number": reg_number}

    headers = {
        "content-type": "application/json",
        "origin": "https://offlinechallan.com",
        "referer": "https://offlinechallan.com/",
        "user-agent": "Mozilla/5.0 (Linux; Android 10)",
        "accept": "*/*"
    }

    r = requests.post(TARGET_URL, json=payload, headers=headers)
    data = r.json()

    data["reg_no"] = reg_number  # add reg no in output

    return jsonify(data), r.status_code


# POST endpoint
@app.route("/vehicle/mobile-no", methods=["POST"])
def post_lookup():
    body = request.get_json()

    if not body or "reg_number" not in body:
        return jsonify({
            "success": False,
            "message": "reg_number is required"
        }), 400

    return fetch_mobile(body["reg_number"])


# GET endpoint
@app.route("/vehicle/mobile-no", methods=["GET"])
def get_lookup():
    reg = request.args.get("reg")

    if not reg:
        return jsonify({
            "success": False,
            "message": "Missing ?reg= parameter"
        }), 400

    return fetch_mobile(reg)


@app.route("/")
def home():
    return "Vehicle API Running ✔"


# Vercel handler
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)
