from flask import Flask, jsonify
from financial_analyzer import analyze_company

app = Flask(__name__)

@app.route("/analyze")
def analyze():
    report = analyze_company()
    return jsonify(report)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)