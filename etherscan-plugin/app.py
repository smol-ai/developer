import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/.well-known/ai-plugin.json")
def serve_plugin_manifest():
    return send_from_directory(".well-known", "ai-plugin.json")

@app.route("/openapi.yaml")
def serve_openapi_spec():
    return send_from_directory(".", "openapi.yaml")

@app.route("/api/etherscan/balance", methods=["GET"])
def get_balance():
    address = request.args.get("address")
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

@app.route("/api/etherscan/transactions", methods=["GET"])
def get_transactions():
    address = request.args.get("address")
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=3333)