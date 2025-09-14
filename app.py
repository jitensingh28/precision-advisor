from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/suggest', methods=['POST'])
def suggest():
    try:
        data = request.get_json(force=True)
        intent = data.get('queryResult', {}).get('intent', {}).get('displayName', '')
        params = data.get('queryResult', {}).get('parameters', {})

        # Intent-based routing
        if intent == 'CaptureID':
            farmer_id = params.get('farmer_id') or params.get('number')
            if not farmer_id:
                return jsonify({"fulfillmentText": "Please say or enter your farmer ID to continue."})
            try:
                farmer_id = int(farmer_id)
            except ValueError:
                return jsonify({"fulfillmentText": "That doesn't seem to be a valid ID. Please try again."})
            df = pd.read_csv('sample_data.csv')
            filtered = df[df['farmer_id'] == farmer_id]
            if filtered.empty:
                return jsonify({"fulfillmentText": f"No data found for farmer ID {farmer_id}. Please try again."})
            row = filtered.iloc[0]
            farmer_name = row.get('farmer_name', 'farmer')
            greeting = f"Hello {farmer_name}! How can I help you with your {row['equipment']} today?"
            return jsonify({"fulfillmentText": greeting})

        # Default: treat as upgrade suggestion (SuggestUpgrade or fallback)
        farmer_id = params.get('farmer_id') or params.get('number')
        if not farmer_id:
            return jsonify({"fulfillmentText": "Please provide your farmer ID."})
        try:
            farmer_id = int(farmer_id)
        except ValueError:
            return jsonify({"fulfillmentText": "That doesn't seem to be a valid ID. Please try again."})
        df = pd.read_csv('sample_data.csv')
        filtered = df[df['farmer_id'] == farmer_id]
        if filtered.empty:
            return jsonify({"fulfillmentText": f"No data found for farmer ID {farmer_id}."})
        row = filtered.iloc[0]
        user_query = data.get('query', '').lower()
        if 'spray' in user_query or 'chemical' in user_query:
            response_text = (
                f"Adding See & Spray to your {row['equipment']} can reduce your chemical usage by {row['potential_savings']}%, "
                f"saving you money every season. The upgrade pays for itself in {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}."
            )
        elif 'planter' in user_query or 'efficiency' in user_query:
            response_text = (
                f"Upgrading your {row['equipment']} to {row['upgrade']} increases planting speed and accuracy, "
                f"boosting efficiency by {row['potential_savings']}%. Payback is just {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}."
            )
        elif 'roi' in user_query or 'return' in user_query:
            response_text = (
                f"Adding {row['upgrade']} to your {row['equipment']} improves guidance and reduces overlap, "
                f"saving {row['potential_savings']}% on fuel and inputs. ROI is typically achieved in {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}."
            )
        elif 'subscription' in user_query:
            if str(row['subscription_available']).lower() == 'yes':
                response_text = (
                    f"You can add {row['upgrade']} to your {row['equipment']} as a subscription, enabling advanced features and remote support. "
                    f"This upgrade costs ${row['upgrade_cost']} and is available as a yearly plan."
                )
            else:
                response_text = f"Currently, there are no subscription options available for your {row['equipment']}."
        elif 'payback' in user_query:
            response_text = (
                f"Upgrading to {row['upgrade']} on your {row['equipment']} has a payback period of {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}, "
                f"with {row['potential_savings']}% savings."
            )
        elif 'feature' in user_query or 'new' in user_query:
            response_text = (
                f"{row['upgrade']} is a new feature for your {row['equipment']}, providing advanced capabilities. "
                f"Upgrade cost is ${row['upgrade_cost']}."
            )
        elif 'productive' in user_query or 'productivity' in user_query:
            response_text = (
                f"Upgrade to {row['upgrade']} to reduce overlap and increase speed, making your {row['equipment']} more productive and efficient."
            )
        elif 'smart' in user_query or 'suggest' in user_query:
            response_text = (
                f"A smart upgrade for your {row['equipment']} is {row['upgrade']}, which can increase productivity and save you {row['potential_savings']}% on operational costs. "
                f"ROI is {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}."
            )
        else:
            response_text = (
                f"The best upgrade for your {row['equipment']} is {row['upgrade']}. "
                f"It can save you {row['potential_savings']}% on input costs, with a payback in just {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}. "
                f"Upgrade cost is ${row['upgrade_cost']}."
            )
            if str(row['subscription_available']).lower() == 'yes':
                response_text += " Subscription options are available."
        return jsonify({"fulfillmentText": response_text})
    except Exception as e:
        import traceback
        error_message = str(e) + "\n" + traceback.format_exc()
        return jsonify({"fulfillmentText": f"Error: {error_message}"})

import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)