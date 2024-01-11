# main.py

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import asyncio
from web3 import Web3
from flask import jsonify

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# GraphQL query URL and limit
url = 'https://api.defikingdoms.com/graphql'
limit = 1000  # Assuming the limit per request is 1000

# Blockchain Providers
KLAYProvider = Web3(Web3.HTTPProvider('https://klaytn.rpc.defikingdoms.com/'))
DFKCProvider = Web3(Web3.HTTPProvider('https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc'))

# Contract addresses
contractAddress = '0x9ed2c155632C042CB8bC20634571fF1CA26f5742'
KLAYAddress = '0xaA8548665bCC12C202d5d0C700093123F2463EA6'

# ABIs
csJewel_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "getTotalLockedAmount",
        "outputs": [
            {"name": "", "type": "uint256"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "getYesterdayAPRData",
        "outputs": [
            {"name": "", "type": "uint256"},
            {"name": "", "type": "uint256"}
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]
burn_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]


# Database Models
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


# Function to fetch data from GraphQL API
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


def fetch_and_calculate_counts():
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


# Blockchain interaction functions



def get_formattedHARM():
    try:
        HARMProvider = Web3(Web3.HTTPProvider('https://api.harmony.one/'))
        HARMJEWEL = HARMProvider.eth.contract(address="0x72Cb10C6bfA5624dD07Ef608027E366bd690048F", abi=burn_ABI)
        balanceHARM = HARMJEWEL.functions.balanceOf('0x000000000000000000000000000000000000dEaD').call()
        return balanceHARM / 1e18
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_totalDFKJ(tokenomicsBurn):
    try:
        DFKCProvider = Web3(Web3.HTTPProvider('https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc'))
        DFKCJEWEL = DFKCProvider.eth.get_balance('0x000000000000000000000000000000000000dEaD') / 1e18
        DFKCValJEWEL = DFKCProvider.eth.get_balance('0x0000000000000000000000000000000000000000') / 1e18
        return DFKCJEWEL + DFKCValJEWEL - tokenomicsBurn
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_formattedKLAY():
    try:
        KLAYProvider = Web3(Web3.HTTPProvider('https://klaytn.rpc.defikingdoms.com/'))
        KLAYJEWEL = KLAYProvider.eth.contract(address="0x30C103f8f5A3A732DFe2dCE1Cc9446f545527b43", abi=burn_ABI)
        balanceKLAY = KLAYJEWEL.functions.balanceOf('0x000000000000000000000000000000000000dEaD').call()
        return balanceKLAY / 1e18
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_totalBurn():
    try:
        formattedHARM = get_formattedHARM()
        formattedKLAY = get_formattedKLAY()
        tokenomicsBurn = 375328483.070918749502816906
        totalDFKJ = get_totalDFKJ(tokenomicsBurn)
        if formattedHARM is not None and formattedKLAY is not None and totalDFKJ is not None:
            return formattedHARM + formattedKLAY + totalDFKJ
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_dfkc_amount():
    try:
        contract = DFKCProvider.eth.contract(address=contractAddress, abi=csJewel_ABI)
        totalLockedAmount = contract.functions.getTotalLockedAmount().call()
        if totalLockedAmount is not None:
            return totalLockedAmount / 1e18
        else:
            return "Error: No data"
    except Exception as e:
        print('Error:', e)
        return "Error occurred"


def get_klay_locked():
    try:
        contract = KLAYProvider.eth.contract(address=KLAYAddress, abi=csJewel_ABI)
        totalKlayLocked = contract.functions.getTotalLockedAmount().call()
        if totalKlayLocked is not None:
            return totalKlayLocked / 1e18
        else:
            return "Error: No data"
    except Exception as e:
        print('Error:', e)
        return "Error occurred"


# Sync Wrappers for Async Functions
def get_balance_sync():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(get_balance())


def get_dfkc_amount_sync():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(get_dfkc_amount())


def get_klay_locked_sync():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(get_klay_locked())


# Flask Routes
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
    if result is not "Error occurred":
        return jsonify({'message': 'DFKC amount fetched', 'result': result})
    else:
        return jsonify({'message': 'Error fetching DFKC amount', 'result': None}), 500


@app.route('/get_klay_locked')
def klay_locked_route():
    result = get_klay_locked()
    if result is not "Error occurred":
        return jsonify({'message': 'Klay locked amount fetched', 'result': result})
    else:
        return jsonify({'message': 'Error fetching Klay locked amount', 'result': None}), 500


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
