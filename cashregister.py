#!/usr/bin/env python3

import csv # used to read csv files 
from pytrie import StringTrie # used to match prefixes in O(log(l)) time where 
# l is the length of the string, better than O(n) time which would be the case
# if we were naively to look through all strings, if there are n strings

products = dict() # dict representing the products, allows O(1) lookup of price 
# informaton based on the product id

trie=StringTrie() # a trie that allows us to look up all the strings matching a
# prefix in O(log(l)) time where l 

# when to program starts it reads the product data from the productdata.csv file
with open('productdata.csv', newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in csvreader:
		id = row[0]
		name = row[1]
		price = row[2]
		category = row[3]
		# add the product to the product map
		products[id] = {"name" : name, "price" : price, "category" : category}
		# add the product to the trie
		trie[id] = (id, name)


while True:
	print()
	print("Please enter a product identifier or type 'q' to quit: ")
	print()

	prefix = input()
	print()
	if prefix == "q" or prefix == "quit" or prefix == "exit":
		break
	got = trie.values(prefix)

	if len(got) == 0:
		print("No matches")
	elif len(got) == 1:
		print("Ringing up: ")
		print()
		print("%-15s %-20s" %("Product ID", "Product name"))		
		print("%-15s %-20s" %(g[0], g[1]))
	else:
		print("Mutiple matching products found: ")
		print()		
		print("%-15s %-20s" %("Product ID", "Product name"))
		for g in got:
			print("%-15s %-20s" %(g[0], g[1]))

		

		


