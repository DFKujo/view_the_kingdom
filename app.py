from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

url = 'https://api.defikingdoms.com/graphql'
limit = 1000  # Assuming the limit per request is 1000

def fetch_data(skip):
    query = f"""
    {{
      bloater_suit: armors(skip: {skip}, where: {{displayId: 50000}}) {{
        id
        displayId
      }}
      karate_gi: armors(skip: {skip}, where: {{displayId: 50001}}) {{
        id
        displayId
      }}
      bloater_head: accessories(skip: {skip}, where: {{displayId: 50000}}) {{
        id
        displayId
      }}
    }}
    """
    result = requests.post(url, json={'query': query})
    return result.json()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BloaterSuit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer)

class KarateGi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer)

class BloaterHead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    count = db.Column(db.Integer)

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

def fetch_and_calculate_counts():
    url = 'https://api.defikingdoms.com/graphql'
    limit = 1000  # Assuming the limit per request is 1000

    total_bloater_suit = 0
    total_karate_gi = 0
    total_bloater_head = 0
    skip = 0

    while True:
        data = fetch_data(skip)
        bloater_suit_count = len(data['data']['bloater_suit'])
        karate_gi_count = len(data['data']['karate_gi'])
        bloater_head_count = len(data['data']['bloater_head'])

        total_bloater_suit += bloater_suit_count
        total_karate_gi += karate_gi_count
        total_bloater_head += bloater_head_count

        if bloater_suit_count < limit and karate_gi_count < limit and bloater_head_count < limit:
            break

        skip += limit

    return {
        'bloater_suit': total_bloater_suit,
        'karate_gi': total_karate_gi,
        'bloater_head': total_bloater_head
    }

if __name__ == '__main__':
    app.run(debug=True)
