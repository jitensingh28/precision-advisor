from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/suggest', methods=['POST'])
def suggest():
    try:
        data = request.get_json(force=True)
        farmer_id = 1  # Or extract from data if needed
        df = pd.read_csv('sample_data.csv')
        row = df[df['farmer_id'] == farmer_id].iloc[0]
        suggestion = {
            "upgrade": str(row['upgrade']),
            "savings": int(row['potential_savings']),
            "cost": int(row['upgrade_cost'])
        }
        response_text = f"Upgrade: {suggestion['upgrade']}, Savings: {suggestion['savings']}%, Cost: ${suggestion['cost']}"
        return jsonify({"fulfillmentText": response_text})
    except Exception as e:
        return jsonify({"fulfillmentText": "Sorry, I couldn't process your request."})

if __name__ == '__main__':
    app.run(port=5000)
