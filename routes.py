from flask import jsonify, render_template
from app import app
from utils import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data/<category>')
def get_data(category):
    if category == 'bloater_suit':
        total_count = fetch_and_calculate_counts()['bloater_suit']
    elif category == 'karate_gi':
        total_count = fetch_and_calculate_counts()['karate_gi']
    elif category == 'bloater_head':
        total_count = fetch_and_calculate_counts()['bloater_head']
    else:
        return jsonify({'error': 'Invalid category'}), 400

    # Placeholder for the change calculations (to be implemented)
    return jsonify({
        'current_count': total_count,
        'change_24h': 0,
        'change_7d': 0,
        'change_30d': 0
    })


@app.route('/get_balance')
def balance_route():
    try:
        formattedHARM = get_formattedHARM()
        formattedKLAY = get_formattedKLAY()
        totalDFKJ = get_totalDFKJ(375328483.070918749502816906)  # Tokenomics burn value
        totalBurn = get_totalBurn()

        if all(value is not None for value in [formattedHARM, formattedKLAY, totalDFKJ, totalBurn]):
            return jsonify({
                "formattedHARM": formattedHARM,
                "totalDFKJ": totalDFKJ,
                "formattedKLAY": formattedKLAY,
                "totalBurn": totalBurn
            })
        else:
            return jsonify({'error': 'Error fetching balance data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_dfkc_amount')
def dfkc_amount_route():
    result = get_dfkc_amount()
    if result != "Error occurred":
        return jsonify({'message': 'DFKC amount fetched', 'result': result})
    else:
        return jsonify({'message': 'Error fetching DFKC amount', 'result': None}), 500


@app.route('/get_klay_locked')
def klay_locked_route():
    result = get_klay_locked()
    if result != "Error occurred":
        return jsonify({'message': 'Klay locked amount fetched', 'result': result})
    else:
        return jsonify({'message': 'Error fetching Klay locked amount', 'result': None}), 500
