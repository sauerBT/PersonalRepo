# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:04:32 2019

@author: brian
"""

import hashlib
import json

reward = 10.0

genesis_block = {
   'previous_hash': '',
   'index': 0,
   'transaction': [],
   'nonce': 23
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Blockgeeks'

def hash_block(block):
   return hashlib.sha256(json.dumps(block).encode()).hexdigest()

"""
-------------------------------------------------------------------------------
 Section 2 
-------------------------------------------------------------------------------
"""

def valid_proof(transactions, last_hash, nonce):
   guess = (str(transactions) + str(last_hash) + str(nonce)).encode()
   guess_hash = hashlib.sha256(guess).hexdigest()
   print(guess_hash)
   return guess_hash[0:2] == '00'

def pow():
   last_block = blockchain[-1]
   last_hash = hash_block(last_block)
   nonce = 0
   while not valid_proof(open_transactions, last_hash, nonce):
       nonce += 1
   return nonce

"""
-------------------------------------------------------------------------------
Section 3 
-------------------------------------------------------------------------------
"""

def get_last_value():
   """ extracting the last element of the blockchain list """
   return(blockchain[-1])

def add_value(recipient, sender=owner, amount=1.0):
   transaction = {'sender': sender,
   'recipient': recipient,
   'amount': amount}
   open_transactions.append(transaction)

"""
-------------------------------------------------------------------------------
Section 4
-------------------------------------------------------------------------------
"""

def mine_block():
   last_block = blockchain[-1]
   hashed_block = hash_block(last_block)
   nonce = pow()
   reward_transaction = {
           'sender': 'MINING',
           'recipient': owner,
           'amount': reward
       }
   open_transactions.append(reward_transaction)
   block = {
       'previous_hash': hashed_block,
       'index': len(blockchain),
       'transaction': open_transactions,
       'nonce': nonce
   }
   blockchain.append(block)

"""
-------------------------------------------------------------------------------
Section 5
-------------------------------------------------------------------------------
"""

def get_transaction_value():
   tx_recipient = input('Enter the recipient of the transaction: ')
   tx_amount = float(input('Enter your transaction amount '))
   return tx_recipient, tx_amount

def get_user_choice():
   user_input = float(input("Please give your choice here: "))
   return user_input

"""
-------------------------------------------------------------------------------
Section 6
-------------------------------------------------------------------------------
"""

def print_block():
   for block in blockchain:
       print("Here is your block")
       print(block)

"""
-------------------------------------------------------------------------------
Section 7
-------------------------------------------------------------------------------
"""

while True:
   print("Choose an option")
   print('Choose 1 for adding a new transaction')
   print('Choose 2 for mining a new block')
   print('Choose 3 for printing the blockchain')
   print('Choose anything else if you want to quit')
   user_choice = get_user_choice()

   if user_choice == 1:
       tx_data = get_transaction_value()
       recipient, amount = tx_data
       add_value(recipient, amount=amount)
       print(open_transactions)

   elif user_choice == 2:
       mine_block()

   elif user_choice == 3:
       print_block()   
   else:
       break