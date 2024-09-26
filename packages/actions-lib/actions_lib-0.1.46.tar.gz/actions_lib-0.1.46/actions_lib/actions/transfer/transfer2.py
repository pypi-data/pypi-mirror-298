from typing import Dict, Any, List, Tuple, Optional
import logging

from web3 import Web3
from eth_utils.abi import function_abi_to_4byte_selector, collapse_if_tuple

from actions_lib.actions.type import Action, ActionData
from actions_lib.utils.contact_tool import get_contact_address

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

token_mapping = {
    "ethereum": {
        "usdc": "0xd10519Aa03FE7Ffb95189B52B74F94Fb33E2C88a",  # USDC on Ethereum
        "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT on Ethereum
    },
    "eth": {
        "usdc": "0xd10519Aa03FE7Ffb95189B52B74F94Fb33E2C88a",  # USDC on Ethereum
        "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT on Ethereum
    },
    "bsc": {
        "usdc": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",  # USDC on BSC
        "usdt": "0x55d398326f99059ff775485246999027b3197955",  # USDT on BSC
    },
    "base": {
        "usdc": "0x45b58118a5374dccf7fd6f3f66c66278ab7473d9",  # USDC on Base
    },
}


allowance_abi = """
[
  {
    "constant": true,
    "inputs": [
      {
        "name": "_owner",
        "type": "address"
      },
      {
        "name": "_spender",
        "type": "address"
      }
    ],
    "name": "allowance",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]
"""

control_contract_abi = [
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "controlTransferFrom",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner_",
        "type": "address"
      }
    ],
    "name": "setOwner",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "token_",
        "type": "address"
      }
    ],
    "name": "setToken",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "token_",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "withdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "stateMutability": "payable",
    "type": "receive"
  },
  {
    "inputs": [],
    "name": "TRANSFER",
    "outputs": [
      {
        "internalType": "bytes4",
        "name": "",
        "type": "bytes4"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "TRANSFERFROM",
    "outputs": [
      {
        "internalType": "bytes4",
        "name": "",
        "type": "bytes4"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]

chain_id_mapping = {
  'base': '0x14a34',
  'ethereum': '0xaa36a7',
  'eth': '0xaa36a7',
  'bsc': '0x38'
}

erc20_approve_abi = """
[{
  "constant": false,
  "inputs": [
    {
      "name": "_spender",
      "type": "address"
    },
    {
      "name": "_value",
      "type": "uint256"
    }
  ],
  "name": "approve",
  "outputs": [
    {
      "name": "",
      "type": "bool"
    }
  ],
  "payable": false,
  "stateMutability": "nonpayable",
  "type": "function"
}]
"""

erc20_transfer_abi = """
[{
  "constant": false,
  "inputs": [
    {
      "name": "recipient",
      "type": "address"
    },
    {
      "name": "amount",
      "type": "uint256"
    }
  ],
  "name": "transfer",
  "outputs": [
    {
      "name": "",
      "type": "bool"
    }
  ],
  "payable": false,
  "stateMutability": "nonpayable",
  "type": "function"
}]
"""

class TransferError(Exception):
    pass

def get_web3_instance(providers: Dict[str, Any], chain: str) -> Web3:
    if chain not in providers:
        raise ValueError(f"Provider for chain {chain} not found")
    return providers[chain]['w3']

def check_allowance(w3: Web3, token_contract, executor: str, spender_address: str, amount: float) -> bool:
    allowance = token_contract.functions.allowance(Web3.to_checksum_address(executor), spender_address).call()
    allowance_normalized = Web3.from_wei(allowance, 'mwei')
    logger.info(f"Allowance: {float(allowance_normalized)}")
    return float(allowance_normalized) >= float(amount)

def get_contact_address_wrapper(redis_client, executor: str, receiver: str, eth_w3: Web3) -> Tuple[int, str]:
    code, res = get_contact_address(redis_client, executor, receiver, eth_w3)
    if code != 200:
        raise TransferError(f"Cannot find {receiver} on contact: {res}")
    return res

from web3.exceptions import ContractLogicError

def handle_auto_transfer(w3: Web3, 
                         eth_w3: Web3, 
                         executor: str, 
                         receiver: str, 
                         amount: float, 
                         token_address: str, 
                         spender_address: str, 
                         control_address: str, 
                         control_contract, 
                         private_key: str,
                         redis_client, 
                         chain: str, 
                         token: str,
                         providers: Dict[str, Any], 
                         **kwargs: Any) -> Dict[str, Any]:
    token_contract = w3.eth.contract(address=token_address, abi=allowance_abi)
    
    if not check_allowance(w3, token_contract, executor, spender_address, amount):
        return handle_insufficient_allowance(w3, executor, receiver, amount, spender_address, token_address, chain, token, **kwargs)

    try:
        receiver_address = get_contact_address_wrapper(redis_client, executor, receiver, eth_w3)
        amount_to_transfer = w3.to_wei(float(amount), 'mwei')
        to_address = w3.to_checksum_address(receiver_address)
        executor_address = w3.to_checksum_address(executor)

        tx_hash = send_transfer_transaction(w3, control_contract, control_address, token_address, 
                                            executor_address, to_address, amount_to_transfer, private_key)
        
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return generate_transfer_result(tx_receipt, tx_hash, chain, providers)

    except TransferError as e:
        return {'result': {"content": str(e), "code": 420}, 'action': None, 'next_action': None}
    except Exception as e:
        return handle_transfer_exception(e, control_contract.abi, w3)

def handle_manual_transfer(w3: Web3, eth_w3: Web3, executor: str, receiver: str, amount: float, 
                           token_address: str, redis_client, chain: str, token: str, **kwargs: Any) -> Dict[str, Any]:
    active_chain_key = f"user:{executor}:active_chain"
    active_chain = redis_client.get(active_chain_key) or "base"

    if active_chain.lower() != chain.lower():
        return handle_incorrect_network(chain, executor, receiver, amount, token, **kwargs)

    try:
        receiver_address = get_contact_address_wrapper(redis_client, executor, receiver, eth_w3)
        amount_to_transfer = w3.to_wei(float(amount), 'mwei')
        to_address = w3.to_checksum_address(receiver_address)

        params = {
            'recipient': to_address,
            'amount': amount_to_transfer,
            'chainId': chain_id_mapping[chain.lower()],
            'contract': token_address,
            'func': 'transfer',
            'abi': erc20_transfer_abi
        }
        action_data = ActionData(func='transfer', group='transfer', params=params)
        action = Action(msg=None, type='wallet', data=action_data.__dict__)

        return {
            'result': {"code": 200, "content": "Manual transfer parameters are constructed"},
            'action': action.__dict__,
            'next_action': None
        }

    except TransferError as e:
        return {'result': {"content": str(e), "code": 420}, 'action': None, 'next_action': None}

def handle_insufficient_allowance(w3: Web3, executor: str, receiver: str, amount: float, spender_address: str, 
                                  token_address: str, chain: str, token: str, **kwargs: Any) -> Dict[str, Any]:
    amount_to_transfer = w3.to_wei(float(amount), 'mwei')
    action_params = {
        "func": "approve",
        "chainId": chain_id_mapping[chain.lower()],
        'contract': token_address,
        '_spender': spender_address,
        '_value': amount_to_transfer,
        'abi': erc20_approve_abi
    }
    action_data = ActionData(func='', group='', params=action_params)
    action = Action(msg=None, type='wallet', data=action_data.__dict__)

    next_params = {
        'receiver': receiver,
        'amount': amount,
        'chain': chain,
        'token': token,
        'run_mode': 'auto'
    }
    next_action_data = ActionData(func='transfer', group='transfer', params=next_params)
    next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)

    return {
        'result': {"code": 200, "content": "Insufficient allowance, proceeding with approval."},
        'action': action.__dict__,
        'next_action': next_action.__dict__
    }

def handle_incorrect_network(chain: str, executor: str, receiver: str, amount: float, token: str, **kwargs: Any) -> Dict[str, Any]:
    params = {"chainId": chain_id_mapping[chain.lower()]}
    action_data = ActionData(func='switch_chain', group='', params=params)
    action = Action(msg=None, type='setting', data=action_data.__dict__)

    next_params = {
        'receiver': receiver,
        'amount': amount,
        'chain': chain,
        'token': token,
        'run_mode': 'manual'
    }
    next_action_data = ActionData(func='transfer', group='transfer', params=next_params)
    next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)

    return {
        'result': {'code': 200, 'content': 'Incorrect network, switching to the correct network for you.'},
        'action': action.__dict__,
        'next_action': next_action.__dict__
    }

def send_transfer_transaction(w3: Web3, control_contract, control_address: str, token_address: str, 
                              from_address: str, to_address: str, amount: int, private_key: str) -> str:
    nonce = w3.eth.get_transaction_count(control_address)
    gas_price = w3.eth.gas_price

    tx = control_contract.functions.transferFromERC20(
        token_address, from_address, to_address, amount).build_transaction({
            'from': control_address,
            'nonce': nonce,
            'gas': 200000,  # Consider making this configurable
            'gasPrice': gas_price,
        })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

def generate_transfer_result(tx_receipt: Dict[str, Any], tx_hash: str, chain: str, providers: Dict[str, Any]) -> Dict[str, Any]:
    status = tx_receipt['status']
    blockchain_explorer = providers[chain.lower()]['scan']
    
    info = {
        "content": generate_markdown_content(status, tx_hash, blockchain_explorer),
        "tx_hash": tx_hash,
        "chain": chain,
        "status": status,
        "code": 200 if status == 1 else 500
    }
    return {'result': info, 'action': None, 'next_action': None}

def handle_transfer_exception(e: Exception, abi: List[Dict[str, Any]], w3: Web3) -> Dict[str, Any]:
    if isinstance(e, ContractLogicError):
        name, params = decode_custom_error(abi, w3, str(e))
        if name:
            message = f"Transfer error, error name: {name}, parameters: {params}"
        else:
            message = f"Transfer failed with unknown contract error: {e}"
    else:
        message = f"Transfer failed with error: {e}"
    
    return {
        'result': {"content": message, "status": 0, "code": 500},
        'action': None, 
        'next_action': None
    }

# Assume these functions are defined elsewhere:
# generate_markdown_content, decode_custom_error

def transfer(receiver, amount, step, run_mode = 'auto', chain = "base", token = "usdc", **kwargs):
    """
    Transfer tokens between addresses.

    :param receiver: The receiver's address
    :param amount: Amount to transfer
    :param step: Step of the transfer process
    :param run_mode: 'auto' or 'manual'
    :param chain: The blockchain to use
    :param token: The token to transfer
    :param kwargs: Additional parameters including providers, executor, etc.
    :return: A dictionary containing the result, action, and next_action
    """
    print(f"receiver: {receiver}, amount: {amount}, run_mode: {run_mode}, chain: {chain}, token: {token}, kwargs: {kwargs}, step: {step}")
    
    # try:
    #     providers = kwargs.get("providers")
    #     if not providers:
    #         raise ValueError("Providers not found in kwargs")

    #     w3 = get_web3_instance(providers, chain.lower())
    #     eth_w3 = get_web3_instance(providers, 'eth')

    #     executor = kwargs.get("executor")
    #     redis_client = kwargs.get("redis_client")
    #     control_address = kwargs.get('control_address')
    #     control_contract = kwargs.get('contract')
    #     private_key = kwargs.get('private_key')
    #     spender_address = kwargs.get('spender_address')

    #     token_address = w3.to_checksum_address(token_mapping[chain.lower()][token.lower()])
        
    #     if run_mode.lower() == 'auto':
    #         return handle_auto_transfer(w3, eth_w3, executor, receiver, amount, token_address, spender_address, 
    #                                     control_address, control_contract, private_key, redis_client, chain, token, providers, **kwargs)
    #     else:
    #         return handle_manual_transfer(w3, eth_w3, executor, receiver, amount, token_address, redis_client, chain, token, **kwargs)
    # except Exception as e:
    #     logger.error(f"Error in transfer: {str(e)}")
    #     return {
    #         'result': {"content": f"Transfer failed: {str(e)}", "code": 500},
    #         'action': None,
    #         'next_action': None
    #     }

    global chain_raw, executor, redis_client, control_address, control_contract, private_key, providers, eth_w3, token_raw, w3, blockchain_explore
    info = None
    chain_raw = chain.lower()
    executor = kwargs.get("executor")
    redis_client = kwargs.get("redis_client")
    control_address = kwargs.get('control_address')
    control_contract = kwargs.get('contract')
    private_key = kwargs.get('private_key')
    spender_address =  kwargs.get('spender_address')
    providers = kwargs.get("providers")
    
    if not providers or chain_raw not in providers:
        raise ValueError(f"Provider for chain {chain} not found")
    
    blockchain_explore = providers[chain_raw]['scan']

    w3 = providers[chain_raw]['w3']
    eth_w3 = providers['eth']['w3']
    token_raw = token
    token = w3.to_checksum_address(token_mapping[chain_raw][token_raw.lower()])
    
    print(f"w3: {w3}", flush=True)

    if run_mode.lower() == 'auto':
      """ check executor approved allowance """
      token_contract = w3.eth.contract(address=token, abi=allowance_abi)
      allowance = token_contract.functions.allowance(Web3.to_checksum_address(executor), spender_address).call()
      allowance_normalized = Web3.from_wei(allowance, 'mwei')
      print(f"allowance_normalized: {float(allowance_normalized)}")
      if float(allowance_normalized) < float(amount):
          amount_to_transfer = w3.to_wei(float(amount), 'mwei')
          action_params = {
            "func": "approve",
            "chainId": chain_id_mapping[chain_raw],
            'contract': token,
            '_spender': spender_address,
            '_value': amount_to_transfer,
            'abi': erc20_approve_abi
          }
          action_data = ActionData(func='', group='', params=action_params)
          action = Action(msg=None, type='wallet', data=action_data.__dict__)

          code, res = get_contact_address(redis_client, executor, receiver, eth_w3)
          if code != 200:
              info = {"content": f"{res}", "code": 420}
              return {
                'result': info,
                'action': None, 
                'next_action': None 
              }
          value = float(amount)
          receiver = res
          to = w3.to_checksum_address(receiver)
          next_params = {
            'receiver': to,
            'amount': amount,
            'chain': chain_raw,
            'token': token_raw,
            'run_mode': run_mode
          }
          next_action_data = ActionData(func='transfer', group='transfer', params=next_params)
          next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)
          return {
            'result': { "code": 200, "content": "Insufficient allowance, proceeding with approval." },
            'action': action.__dict__,
            'next_action': next_action.__dict__
          }
      code, res = get_contact_address(redis_client, executor, receiver, eth_w3)
      if code != 200:
          info = {"content": f"Cannot find {receiver} on contact", "code": 420}
          return {
            'result': info,
            'action': None, 
            'next_action': None 
          }
      value = float(amount)
      amount_to_transfer = w3.to_wei(value, 'mwei')  # USDT uses 6 decimals
      receiver = res
      to = w3.to_checksum_address(receiver)
      executor = w3.to_checksum_address(executor)

      print(f"to: {to}, executor: {executor}")
      tx_hash = None
      try:
          nonce = w3.eth.get_transaction_count(control_address)
          current_gas_price = w3.eth.gas_price
          replacement_gas_price = current_gas_price
          tx = control_contract.functions.transferFromERC20(
              token, executor, to, amount_to_transfer).build_transaction({
                'from': control_address,
                'nonce': nonce,
                'gas': 200000,  # Adjust gas limit
                'gasPrice': replacement_gas_price,  # Adjust gas price
              })
          pk = private_key
          signed_tx = w3.eth.account.sign_transaction(tx, pk)
          send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
          tx_hash = send_tx.hex()
          tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
          status = 200
          message = "success"
          if tx_receipt['status'] == 0:
              status = 500
              message = "failed"
          info = {
            "content": generate_markdown_content(tx_receipt['status'], tx_hash, blockchain_explore),
            "tx_hash": tx_hash,
            "chain": chain_raw,
            "status": tx_receipt['status'],
            "code": status
          }
          return { 
            'result': info, 
            'action': None, 
            'next_action': None 
          }
      except Exception as e:
          name, params = decode_custom_error(control_contract_abi, w3, str(e))
          if not name:
              # Note: If unknown error expose, check:
              # 1. if abi.json is the latest
              # 2. what error is exposed, how it happens
              message = f"Transfer usdt failed with unknown error: {e}"
          else:
              message = f"Transfer usdt error, error name: {name}, parameters: {params}"
          info = {"content": message, "status": 0, "code": 500}
          return {
            'result': info,
            'action': None, 
            'next_action': None
          }
    else:
      """ check executor current active chain """
      active_chain_key = f"user:{executor}:active_chain"
      active_chain = redis_client.get(active_chain_key)
      if not active_chain:
        active_chain = "base"
      if active_chain.lower() != chain_raw:
          params = {
            "chainId": chain_id_mapping[chain_raw]
          }
          action_data = ActionData(func='switch_chain', group='', params=params)
          action = Action(msg=None, type='setting', data=action_data.__dict__)

          code, res = get_contact_address(redis_client, executor, receiver, eth_w3)
          if code != 200:
              info = {"content": f"Cannot find {receiver} on contact", "code": 420}
              return {
                'result': info,
                'action': None, 
                'next_action': None
              }
          value = float(amount)
          receiver = res
          to = w3.to_checksum_address(receiver)
          params = {
            'receiver': to,
            'amount': amount,
            'chain': chain_raw,
            'token': token_raw,
            'run_mode': run_mode
          }
          next_action_data = ActionData(func='transfer', group='transfer', params=params)
          next_action = Action(msg=None, type='backend', data=next_action_data.__dict__)

          return {
            'result': { 'code': 200, 'content': 'Incorrect network, switching to the correct network for you.' },
            'action': action.__dict__,
            'next_action': next_action.__dict__
          }
      else:
          code, res = get_contact_address(redis_client, executor, receiver, eth_w3)
          if code != 200:
              info = {"content": f"Cannot find {receiver} on contact", "code": 420}
              return {
                'result': info,
                'action': None,
                'next_action': None
              }
          value = float(amount)
          amount_to_transfer = w3.to_wei(value, 'mwei')  # USDT uses 6 decimals
          receiver = res
          to = w3.to_checksum_address(receiver)
          params = {
            'recipient': to,
            'amount': amount_to_transfer,
            'chainId': chain_id_mapping[chain_raw],
            'contract': token,
            'func': 'transfer',
            'abi': erc20_transfer_abi
          }
          action_data = ActionData(func='transfer', group='transfer', params=params)
          action = Action(msg=None, type='wallet', data=action_data.__dict__)
          return {
            'result': { "code": 200, "content": "Manual transfer parameters are constructed" },
            'action': action.__dict__,
            'next_action': None
          }

def generate_markdown_content(status, hash_value, blockchain_explore):
    if status == 1:
        return f"Transfer successful. You can check the transaction on [blockchain explorer]({blockchain_explore}{hash_value})"
    else:
        return f"Transfer failed. You can check the transaction on [blockchain explorer]({blockchain_explore}{hash_value})"

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
