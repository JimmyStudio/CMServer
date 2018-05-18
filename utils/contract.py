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
# from utils import etc

default_pw = '123'

config = {
    "abi": [
    {
      "inputs": [],
      "payable": False,
      "stateMutability": "nonpayable",
      "type": "constructor"
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
    "address": "0xb925cf2f15af95d968e0cbb82cea4f67b60108f2",
    # "address": "0x5bab432047d74cbe78c37dea0d18ba8a50f9f790", # in server
}

# def update_copyright(ipfs_address,id_in_server,cp_hash,owner,share_integer,share_decimals):
#     transact_hash = contract_instance.update_copyright(ipfs_address,id_in_server,cp_hash,owner,share_integer,share_decimals,transact={'from': owner})
#     return transact_hash
#
# def delete_copyright(id_in_server):
#     transact_hash = contract_instance.delete_copyright(id_in_server,transact={'from': owner})
#     return transact_hash
#
# def get_copyright_share(id_in_server,owner):
#     transact_hash = contract_instance.get_copyright_share(id_in_server, owner, transact={'from': owner})
#     return transact_hash
#

def new_account():
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    addr = web3.personal.newAccount(default_pw)
    web3.personal.unlockAccount(addr, default_pw)
    return addr

def eth_balance(addr):
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    return web3.eth.getBalance(addr)/1000000000000000000

def transaction_info(th):
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    return web3.eth.getTransaction(th)

def block_number():
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    return web3.eth.blockNumber

def block_info(block_number):
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    return web3.eth.getBlock(block_number)

def balance_of(user):
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    contract_instance = web3.eth.contract(address=config['address'],
                                          abi=config['abi'],
                                          ContractFactoryClass=ConciseContract)
    return contract_instance.balance_of(user)

def transfer(_from, _to, _value):
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    owner = web3.eth.accounts[0]
    contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'],
                                          ContractFactoryClass=ConciseContract)
    transact_hash = contract_instance.transfer(_from, _to, _value, transact={'from': owner})
    return transact_hash

def generate_token(_to, _value):
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    owner = web3.eth.accounts[0]
    contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'],
                                          ContractFactoryClass=ConciseContract)
    transact_hash = contract_instance.generate_token(_to, _value, transact={'from': owner})
    return transact_hash

if __name__ == "__main__":
    web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
    owner = web3.eth.accounts[0]
    print(eth_balance(owner))
    # print(generate_token(owner, 100000))
    # print(balance_of(owner))
