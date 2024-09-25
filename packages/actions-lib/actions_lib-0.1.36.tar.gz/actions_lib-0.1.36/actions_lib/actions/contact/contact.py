from web3 import Web3
from ens import ENS

from actions_lib.utils.contact_tool import redis_add_contact, redis_show_contact

def add_contact(name, address, step, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    providers = kwargs.get("providers")
    provider = Web3.HTTPProvider(providers['ethereum'])
    provider.middlewares.clear()
    w3 = Web3(provider)
    ens_name = None
    try:
        ns = ENS.from_web3(w3)
        ens_name = ns.name(address)
        if ens_name:
            print(f"The ENS name for the address {address} is: {ens_name}")
        else:
            print(f"No ENS name found for the address {address}")
    except Exception as e:
        print(f"Get address({address}) ens error: {e}")
    code, res = redis_add_contact(redis_client, executor, name, address, ens_name)
    return {
        'result': { 'code': code, 'content': res },
        'action': None, 
        'next_action': None 
    }

def show_contact_by_name(name, step, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    code, res = redis_show_contact(redis_client, executor, name)
    return {
        'result': { 'code': code, 'content': res },
        'action': None, 
        'next_action': None 
    } 

def show_all_contact(step, **kwargs):
    redis_client = kwargs.get('redis_client')
    executor =  kwargs.get('executor')
    code, res = redis_show_contact(redis_client, executor, None)
    return {
        'result': { 'code': code, 'content': res },
        'action': None, 
        'next_action': None 
    }  