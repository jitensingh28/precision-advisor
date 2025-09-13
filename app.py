from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.json
    farmer_id = data.get('farmer_id', 1)
    df = pd.read_csv('sample_data.csv')
    row = df[df['farmer_id'] == farmer_id].iloc[0]
    suggestion = {
        "upgrade": str(row['upgrade']),
        "savings": int(row['potential_savings']),
        "cost": int(row['upgrade_cost'])
    }
    return jsonify(suggestion)

if __name__ == '__main__':
    app.run(port=5000)
