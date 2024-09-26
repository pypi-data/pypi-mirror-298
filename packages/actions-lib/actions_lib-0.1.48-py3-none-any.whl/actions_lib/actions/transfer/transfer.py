from typing import Tuple, Dict, Any
from web3 import Web3
from eth_utils.abi import function_abi_to_4byte_selector, collapse_if_tuple
from actions_lib.actions.type import Action, ActionData
from actions_lib.utils.contact_tool import get_contact_address

# Constants
TOKEN_MAPPING = {
    "ethereum": {
        "usdc": "0xd10519Aa03FE7Ffb95189B52B74F94Fb33E2C88a",
        "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    },
    "eth": {
        "usdc": "0xd10519Aa03FE7Ffb95189B52B74F94Fb33E2C88a",
        "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    },
    "bsc": {
        "usdc": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "usdt": "0x55d398326f99059ff775485246999027b3197955",
    },
    "base": {
        "usdc": "0x45b58118a5374dccf7fd6f3f66c66278ab7473d9",
    },
}

CHAIN_ID_MAPPING = {
    'base': '0x14a34',
    'ethereum': '0xaa36a7',
    'eth': '0xaa36a7',
    'bsc': '0x38'
}

# ABIs
ALLOWANCE_ABI = """[{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]"""

CONTROL_CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "controlTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {"inputs": [{"internalType": "address", "name": "owner_", "type": "address"}], "name": "setOwner", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "token_", "type": "address"}], "name": "setToken", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {"inputs": [{"internalType": "address", "name": "token_", "type": "address"}, {"internalType": "uint256", "name": "value", "type": "uint256"}], "name": "withdraw", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"stateMutability": "payable", "type": "receive"},
    {"inputs": [], "name": "TRANSFER", "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "TRANSFERFROM", "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}], "stateMutability": "view", "type": "function"},
]

ERC20_APPROVE_ABI = """[{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]"""

ERC20_TRANSFER_ABI = """[{"constant":false,"inputs":[{"name":"recipient","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]"""

def transfer(receiver: str, amount: float, step: any, run_mode: str = 'auto', chain: str = "base", token: str = "usdc", **kwargs: Any) -> Dict[str, Any]:
    print(f"receiver: {receiver}, amount: {amount}, run_mode: {run_mode}, chain: {chain}, token: {token}, kwargs: {kwargs}, step: {step}")
    
    chain_raw = chain.lower()
    executor = kwargs.get("executor")
    redis_client = kwargs.get("redis_client")
    control_address = kwargs.get('control_address')
    control_contract = kwargs.get('contract')
    private_key = kwargs.get('private_key')
    spender_address = kwargs.get('spender_address')
    providers = kwargs.get("providers")
    
    if not providers or chain_raw not in providers:
        raise ValueError(f"Provider for chain {chain} not found")
    
    blockchain_explore = providers[chain_raw]['scan']
    w3 = providers[chain_raw]['w3']
    eth_w3 = providers['eth']['w3']
    token_raw = token.lower()
    token_address = w3.to_checksum_address(TOKEN_MAPPING[chain_raw][token_raw])
    
    print(f"w3: {w3}", flush=True)

    if run_mode.lower() == 'auto':
        return handle_auto_transfer(w3, eth_w3, executor, receiver, amount, token_address, spender_address, control_address, control_contract, private_key, redis_client, chain_raw, token_raw, blockchain_explore)
    else:
        return handle_manual_transfer(w3, executor, receiver, amount, token_address, redis_client, chain_raw, token_raw)

def handle_auto_transfer(w3, eth_w3, executor, receiver, amount, token_address, spender_address, control_address, control_contract, private_key, redis_client, chain_raw, token_raw, blockchain_explore):
    token_contract = w3.eth.contract(address=token_address, abi=ALLOWANCE_ABI)
    allowance = token_contract.functions.allowance(Web3.to_checksum_address(executor), spender_address).call()
    allowance_normalized = Web3.from_wei(allowance, 'mwei')
    print(f"allowance_normalized: {float(allowance_normalized)}")
    
    if float(allowance_normalized) < float(amount):
        return handle_insufficient_allowance(w3, executor, receiver, amount, spender_address, token_address, chain_raw, token_raw, redis_client)

    code, receiver_address = get_contact_address(redis_client, executor, receiver, eth_w3)
    if code != 200:
        return {'result': {"content": f"Cannot find {receiver} on contact", "code": 420}, 'action': None, 'next_action': None}

    amount_to_transfer = w3.to_wei(float(amount), 'mwei')
    to = w3.to_checksum_address(receiver_address)
    executor = w3.to_checksum_address(executor)

    print(f"to: {to}, executor: {executor}")
    
    try:
        tx_hash = send_transaction(w3, control_contract, control_address, token_address, executor, to, amount_to_transfer, private_key)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        status = 200 if tx_receipt['status'] == 1 else 500
        info = {
            "content": generate_markdown_content(tx_receipt['status'], tx_hash.hex(), blockchain_explore),
            "tx_hash": tx_hash.hex(),
            "chain": chain_raw,
            "status": tx_receipt['status'],
            "code": status
        }
        return {'result': info, 'action': None, 'next_action': None}
    except Exception as e:
        return handle_transaction_error(e, control_contract, w3)

def handle_manual_transfer(w3, executor, receiver, amount, token_address, redis_client, chain_raw, token_raw):
    active_chain_key = f"user:{executor}:active_chain"
    active_chain = redis_client.get(active_chain_key) or "base"
    
    if active_chain.lower() != chain_raw:
        return handle_incorrect_network(w3, executor, receiver, amount, chain_raw, token_raw, redis_client)
    
    code, receiver_address = get_contact_address(redis_client, executor, receiver, w3)
    if code != 200:
        return {'result': {"content": f"Cannot find {receiver} on contact", "code": 420}, 'action': None, 'next_action': None}

    amount_to_transfer = w3.to_wei(float(amount), 'mwei')
    to = w3.to_checksum_address(receiver_address)
    params = {
        'recipient': to,
        'amount': amount_to_transfer,
        'chainId': CHAIN_ID_MAPPING[chain_raw],
        'contract': token_address,
        'func': 'transfer',
        'abi': ERC20_TRANSFER_ABI
    }
    action_data = ActionData(func='transfer', group='transfer', params=params)
    action = Action(msg=None, type='wallet', data=action_data.__dict__)
    return {'result': {"code": 200, "content": "Manual transfer parameters are constructed"}, 'action': action.__dict__, 'next_action': None}

def handle_insufficient_allowance(w3, executor, receiver, amount, spender_address, token_address, chain_raw, token_raw, redis_client):
    amount_to_transfer = w3.to_wei(float(amount), 'mwei')
    action_params = {
        "func": "approve",
        "chainId": CHAIN_ID_MAPPING[chain_raw],
        'contract': token_address,
        '_spender': spender_address,
        '_value': amount_to_transfer,
        'abi': ERC20_APPROVE_ABI
    }
    action_data = ActionData(func='', group='', params=action_params)
    action = Action(msg=None, type='wallet', data=action_data.__dict__)

    code, receiver_address = get_contact_address(redis_client, executor, receiver, w3)
    if code != 200:
        return {'result': {"content": f"{receiver_address}", "code": 420}, 'action': None, 'next_action': None}

    next_params = {
        'receiver': w3.to_checksum_address(receiver_address),
        'amount': amount,
        'chain': chain_raw,
        'token': token_raw,
        'run_mode': 'auto'
    }
    next_action_data = ActionData(func='transfer', group='transfer', params=next_params)
    next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)
    return {'result': {"code": 200, "content": "Insufficient allowance, proceeding with approval."}, 'action': action.__dict__, 'next_action': next_action.__dict__}

def handle_incorrect_network(w3, executor, receiver, amount, chain_raw, token_raw, redis_client):
    params = {"chainId": CHAIN_ID_MAPPING[chain_raw]}
    action_data = ActionData(func='switch_chain', group='', params=params)
    action = Action(msg=None, type='setting', data=action_data.__dict__)

    code, receiver_address = get_contact_address(redis_client, executor, receiver, w3)
    if code != 200:
        return {'result': {"content": f"Cannot find {receiver} on contact", "code": 420}, 'action': None, 'next_action': None}

    next_params = {
        'receiver': w3.to_checksum_address(receiver_address),
        'amount': amount,
        'chain': chain_raw,
        'token': token_raw,
        'run_mode': 'manual'
    }
    next_action_data = ActionData(func='transfer', group='transfer', params=next_params)
    next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)

    return {'result': {'code': 200, 'content': 'Incorrect network, switching to the correct network for you.'}, 'action': action.__dict__, 'next_action': next_action.__dict__}

def send_transaction(w3, control_contract, control_address, token, executor, to, amount_to_transfer, private_key):
    nonce = w3.eth.get_transaction_count(control_address)
    current_gas_price = w3.eth.gas_price
    tx = control_contract.functions.transferFromERC20(
        token, executor, to, amount_to_transfer).build_transaction({
            'from': control_address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': current_gas_price,
        })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    return w3.eth.send_raw_transaction(signed_tx.rawTransaction)

def handle_transaction_error(e, control_contract, w3):
    name, params = decode_custom_error(control_contract.abi, w3, str(e))
    if not name:
        message = f"Transfer failed with unknown error: {e}"
    else:
        message = f"Transfer error, error name: {name}, parameters: {params}"
    return {'result': {"content": message, "status": 0, "code": 500}, 'action': None, 'next_action': None}

def generate_markdown_content(status, hash_value, blockchain_explore):
    status_text = "successful" if status == 1 else "failed"
    return f"Transfer {status_text}. You can check the transaction on [blockchain explorer]({blockchain_explore}{hash_value})"

def decode_custom_error(contract_abi, w3, error) -> Tuple[str, str]:
    # Parse error content, the error content must look like:
    # "Call method: submitServiceProof,xxxxx,error:('xxxxxx','xxxxxxx')"
    tmp_array = error.split(":")
    if len(tmp_array) != 3:
        return None, None
    param_str = tmp_array[2]
    param_str = param_str.replace("(","")
    param_str = param_str.replace(")","")
    param_str = param_str.replace(",","")
    param_str = param_str.replace("'","")
    errors = param_str.split()

    for error in [abi for abi in contract_abi if abi["type"] == "error"]:
        # Get error signature components
        name = error["name"]
        data_types = [collapse_if_tuple(abi_input) for abi_input in error.get("inputs", [])]
        error_signature_hex = function_abi_to_4byte_selector(error).hex()
        # Find match signature from error
        for error in errors:
            if error_signature_hex.casefold() == error[2:10].casefold():
                params = ','.join([str(x) for x in w3.codec.decode(data_types,bytes.fromhex(error[10:]))])
                #decoded = "%s(%s)" % (name , str(params))
                return name, params
    return None, None #try other contracts until result is not None since error may be raised from another called contract