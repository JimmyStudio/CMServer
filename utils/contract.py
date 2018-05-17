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
    "address": "0xbfa2e6a3096f9c9b94b8b135fc790b6539176cc0",
    # "address": "0xe7afd0b0450b0e6fc1d717398b1ade2032128e3d", # in server
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

    block = block_info(1)
    print(block)

    tran = transaction_info('0x630a9297e03f280db326fc874d87bfa9d91237abaa63989fb22af0788196597d')
    print(tran)

    # print(generate_token(owner, 100000))
    # print(balance_of(owner))
