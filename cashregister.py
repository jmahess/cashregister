#!/usr/bin/env python3

import csv # used to read csv files 
from pytrie import StringTrie # used to match prefixes in O(log(l)) time where 
# l is the length of the string, better than O(n) time which would be the case
# if we were naively to look through all strings, if there are n strings

products = dict() # dict representing the products, allows O(1) lookup of price 
# informaton based on the product id

rungup = set() # this stores the products that we have rung up

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
		trie[id] = (id, name, price)


while True:
	print()
	print("Please enter a product identifier or type 'h' for help: ")
	print()

	prefix = input()
	print()

	if prefix == "h" or prefix == "help":
		print("Use the following commands:")
		print()
		print("%-15s %-40s" %("Command", "Description"))
		print("%-15s %-40s" %("help", "List help"))
		print("%-15s %-40s" %("quit", "Quit / exit the program"))
		print("%-15s %-40s" %("rungup", "List the rung up items"))
		print("%-15s %-40s" %("total", "Calculate the total bill and finish"))
		continue

	# functionality to total up and calculate taxes
	if prefix == "t" or prefix == "total":
		print("%-18s %-9s" %("Product name", "Price"))	
		total = 0 # the total amount
		totalCountyTaxable = 0 # the amount taxable by the county
		for r in rungup:	
			total += float(products[r]["price"]) # add up the total amounts
			if products[r]["category"] != "g":
				totalCountyTaxable += float(products[r]["price"]) # only add non grocery items to 
				# the county taxable amount
		print()
		print("%-18s %-9s" %("Subtotal: ", total))
		# add up the tax, 6.3% state + 2% city (8.3%) 
		# on everything, and 0.7% county on non grocery items. Round to 2 decimal places, dollars and cents		
		statetax = round(total*0.063)
		countytax = round(totalCountyTaxable*0.007, 2)
		citytax = round(total*0.02)
		tax = statetax + countytax + citytax
		print("%-18s %-9s" %("Tax: ", tax))
		print("%-18s %-9s" %("Total due: ", round(tax + total, 2)))
		print()

		print("Please enter the amount paid by the customer:")
		customerAmount = input()
		print()
		print("Receipt:")
		print()
		print("%-18s %-18s %-10s %-17s" %("Product name", "Product identifier", "Price", "Tax category"))	

		for id in rungup:	
			print("%-18s %-18s %-10s %-17s" %(products[id]["name"], id, products[id]["price"], products[id]["category"]))	

		print()
		print("%-18s %-9s" %("State tax: ", statetax))
		print("%-18s %-9s" %("Total due: ", round(tax + total, 2)))
		print()



		break

	# exit the program functionality
	if prefix == "q" or prefix == "quit" or prefix == "exit":
		break

	# functionlity to list the rung up items. Not in the problem set but useful to see
	# what has been rung up so far
	if prefix == "r" or prefix == "rungup":
		print("Rung up items so far: ")
		print()
		print("%-18s %-9s" %("Product name", "Price"))	
		for r in rungup:	
			print("%-18s %-9s" %(products[r]["name"], products[r]["price"]))		
		continue

	got = trie.values(prefix)

	if len(got) == 0:
		print("No matches")
	elif len(got) == 1:
		print("Ringing up: ")
		print()
		print("%-18s %-9s" %("Product name", "Price"))		
		row = got[0]
		id = row[0]
		name = row[1]
		price = row[2]
		print("%-18s %-9s" %(name, price))
		rungup.add(id) # add the product ID to the set of rung up items
	else:
		print("Mutiple matching products found: ")
		print()		
		print("%-15s %-20s" %("Product ID", "Product name"))
		for g in got:
			print("%-15s %-20s" %(g[0], g[1]))

		

		


