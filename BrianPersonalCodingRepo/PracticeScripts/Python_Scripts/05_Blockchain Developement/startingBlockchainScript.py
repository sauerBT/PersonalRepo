# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:45:50 2019

@author: brian
"""
blockchain = [];
def get_last_value():

   """ extracting the last element of the blockchain list """

   return(blockchain[-1])



def add_value(transaction_amount, last_transaction=[1]):
   blockchain.append([last_transaction, transaction_amount])
""" Section 2 """

def get_transaction_value():
   user_value = float(input('Enter your transaction amount '))
   return user_value

def get_user_choice():
   user_input = input("Please give your choice here: ")
   return user_input
""" Section 3 """

def print_block():
   for block in blockchain:
       print("Here is your block")
       print(block)

""" Section 4 """

def verify_chain():
   index = 0
   valid = True
   for block in blockchain:
       if index == 0:
           index += 1
           continue
       elif block[0] == blockchain[index - 1]:
           valid = True
       else:
           valid = False
           break
       index += 1
   return valid
""" Section 5 """

tx_amount = get_transaction_value()
add_value(tx_amount)
while True:
   print("Choose an option")
   print('Choose 1 for adding a new transaction')
   print('Choose 2 for printing the blockchain')
   print('Choose 3 if you want to manipulate the data')
   print('Choose anything else if you want to quit')
   user_choice = get_user_choice()
   
   if user_choice == 1:
       tx_amount = get_transaction_value()
       add_value(tx_amount, get_last_value())   
   elif user_choice == 2:
       print_block()
   elif user_choice == 3:
       if len(blockchain) >= 1:
           blockchain[0] = 2
   else:
       break
   if not verify_chain():
       print('Blockchain manipulated')
       break