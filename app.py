from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/suggest', methods=['POST'])
def suggest():
    try:
        data = request.get_json(force=True)
        # For demo, use farmer_id=1 or extract from data if provided
        farmer_id = data.get('farmer_id', 1)
        df = pd.read_csv('sample_data.csv')
        row = df[df['farmer_id'] == farmer_id].iloc[0]
        # Get user question if available
        user_query = data.get('query', '').lower()
        # Template selection based on keywords in user_query
        if 'spray' in user_query or 'chemical' in user_query:
            # Spraying cost savings or chemical reduction
            response_text = (
                f"Adding See & Spray to your {row['equipment']} can reduce your chemical usage by {row['potential_savings']}%, "
                f"saving you money every season. The upgrade pays for itself in {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}."
            )
        elif 'planter' in user_query or 'efficiency' in user_query:
            # Planter efficiency
            response_text = (
                f"Upgrading your {row['equipment']} to {row['upgrade']} increases planting speed and accuracy, "
                f"boosting efficiency by {row['potential_savings']}%. Payback is just {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}."
            )
        elif 'roi' in user_query or 'return' in user_query:
            # Tractor ROI
            response_text = (
                f"Adding {row['upgrade']} to your {row['equipment']} improves guidance and reduces overlap, "
                f"saving {row['potential_savings']}% on fuel and inputs. ROI is typically achieved in {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}."
            )
        elif 'subscription' in user_query:
            # Subscription options
            if str(row['subscription_available']).lower() == 'yes':
                response_text = (
                    f"You can add {row['upgrade']} to your {row['equipment']} as a subscription, enabling advanced features and remote support. "
                    f"This upgrade costs ${row['upgrade_cost']} and is available as a yearly plan."
                )
            else:
                response_text = f"Currently, there are no subscription options available for your {row['equipment']}."
        elif 'payback' in user_query:
            # Payback period
            response_text = (
                f"Upgrading to {row['upgrade']} on your {row['equipment']} has a payback period of {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}, "
                f"with {row['potential_savings']}% savings."
            )
        elif 'feature' in user_query or 'new' in user_query:
            # New features
            response_text = (
                f"{row['upgrade']} is a new feature for your {row['equipment']}, providing advanced capabilities. "
                f"Upgrade cost is ${row['upgrade_cost']}."
            )
        elif 'productive' in user_query or 'productivity' in user_query:
            # Productivity boost
            response_text = (
                f"Upgrade to {row['upgrade']} to reduce overlap and increase speed, making your {row['equipment']} more productive and efficient."
            )
        elif 'smart' in user_query or 'suggest' in user_query:
            # Smart upgrade suggestion
            response_text = (
                f"A smart upgrade for your {row['equipment']} is {row['upgrade']}, which can increase productivity and save you {row['potential_savings']}% on operational costs. "
                f"ROI is {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}."
            )
        else:
            # Default: Best upgrade recommendation
            response_text = (
                f"The best upgrade for your {row['equipment']} is {row['upgrade']}. "
                f"It can save you {row['potential_savings']}% on input costs, with a payback in just {row['roi_seasons']} season{'s' if row['roi_seasons'] > 1 else ''}. "
                f"Upgrade cost is ${row['upgrade_cost']}."
            )
            if str(row['subscription_available']).lower() == 'yes':
                response_text += " Subscription options are available."
        return jsonify({"fulfillmentText": response_text})
    except Exception as e:
        return jsonify({"fulfillmentText": "Sorry, I couldn't process your request."})

if __name__ == '__main__':
    app.run(port=5000)
