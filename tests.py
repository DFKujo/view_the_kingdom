from web3 import Web3

# ABI for the contract
ERC20_ABI = [
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

# Providers
KLAYProvider = Web3(Web3.HTTPProvider('https://klaytn.rpc.defikingdoms.com/'))
DFKCProvider = Web3(Web3.HTTPProvider('https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc'))

# Contract addresses
contractAddress = '0x9ed2c155632C042CB8bC20634571fF1CA26f5742'
KLAYAddress = '0xaA8548665bCC12C202d5d0C700093123F2463EA6'

async def get_dfkc_amount():
    try:
        contract = DFKCProvider.eth.contract(address=contractAddress, abi=ERC20_ABI)
        totalLockedAmount = contract.functions.getTotalLockedAmount().call()
        apr_data = contract.functions.getYesterdayAPRData().call()
        formattedAmount = totalLockedAmount / 1e18
        print('Total Locked on DFKChain:', formattedAmount)
        print('APR:', apr_data)

    except Exception as e:
        print('Error:', e)

async def get_klay_locked():
    try:
        contract = KLAYProvider.eth.contract(address=KLAYAddress, abi=ERC20_ABI)
        totalKlayLocked = contract.functions.getTotalLockedAmount().call()
        formattedAmount = totalKlayLocked / 1e18
        print('Total Locked Klay:', formattedAmount)

    except Exception as e:
        print('Error:', e)

# Running the functions
import asyncio
asyncio.run(get_dfkc_amount())
asyncio.run(get_klay_locked())
