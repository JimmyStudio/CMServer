# -*- coding: utf-8 -*-

'''
author:       Jimmy
contact:      234390130@qq.com
file:         contract.py
time:         2018/3/19 下午5:50
description: 

'''

__author__ = 'Jimmy'

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

config = {
    "abi": [
        {
            "inputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "name": "ipfs_address",
                    "type": "string"
                },
                {
                    "name": "id_in_server",
                    "type": "string"
                },
                {
                    "name": "cp_hash",
                    "type": "string"
                },
                {
                    "name": "owner",
                    "type": "address"
                },
                {
                    "name": "share_integer",
                    "type": "uint256"
                },
                {
                    "name": "share_decimals",
                    "type": "uint256"
                }
            ],
            "name": "update_copyright",
            "outputs": [
                {
                    "name": "",
                    "type": "bool"
                }
            ],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "name": "id_in_server",
                    "type": "string"
                }
            ],
            "name": "delete_copyright",
            "outputs": [
                {
                    "name": "",
                    "type": "bool"
                }
            ],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "name": "id_in_server",
                    "type": "string"
                },
                {
                    "name": "owner",
                    "type": "address"
                }
            ],
            "name": "get_copyright_share",
            "outputs": [
                {
                    "name": "",
                    "type": "uint256"
                },
                {
                    "name": "",
                    "type": "uint256"
                },
                {
                    "name": "",
                    "type": "bool"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [
                {
                    "name": "_user",
                    "type": "address"
                }
            ],
            "name": "balance_of",
            "outputs": [
                {
                    "name": "balance",
                    "type": "uint256"
                }
            ],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "name": "_from",
                    "type": "address"
                },
                {
                    "name": "_to",
                    "type": "address"
                },
                {
                    "name": "_value",
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
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {
                    "name": "_to",
                    "type": "address"
                },
                {
                    "name": "_value",
                    "type": "uint256"
                }
            ],
            "name": "generate_token",
            "outputs": [
                {
                    "name": "",
                    "type": "bool"
                }
            ],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ],
    "address": "0x3855e692db75e5cd1e1e5e947a9dc6039ecbc0a6",
}

web3 = Web3(HTTPProvider('http://localhost:8545'))
owner = web3.eth.accounts[0]
contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'],ContractFactoryClass=ConciseContract)



def update_copyright(ipfs_address,id_in_server,cp_hash,owner,share_integer,share_decimals):
    transact_hash = contract_instance.update_copyright(ipfs_address,id_in_server,cp_hash,owner,share_integer,share_decimals,transact={'from': owner})
    return transact_hash

def delete_copyright(id_in_server):
    transact_hash = contract_instance.delete_copyright(id_in_server,transact={'from': owner})
    return transact_hash

def get_copyright_share(id_in_server,owner):
    transact_hash = contract_instance.get_copyright_share(id_in_server, owner, transact={'from': owner})
    return transact_hash

def balance_of(user):
    return contract_instance.balance_of(user)

def transfer(_from, _to, _value):
    transact_hash = contract_instance.transfer(_from, _to, _value, transact={'from': owner})
    return transact_hash

def generate_token(_to, _value):
    transact_hash = contract_instance.generate_token(_to, _value, transact={'from': owner})
    return transact_hash

if __name__ == "__main__":
    generate_token(owner, 100000)
    print(balance_of(owner))
