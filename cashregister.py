#!/usr/bin/env python3

import csv # used to read csv files 
from pytrie import StringTrie # used to match prefixes in better than O(n) time.
# O(n) time would be the case if we did not use a trie and instead naively looked
#  through all the n strings and check one by one

products = dict() # a dict is a hashmap representing the products, allows O(1) lookup of product price 
# informaton based on the product id

rungup = set() # this stores the products that we have rung up and allows O(1) insertion time

trie=StringTrie() # a trie that allows us to look up all the strings matching a
# prefix in faster than O(n) time where n is the number of strings

# when to program starts it reads the product data from the productdata.csv file
with open('productdata.csv', newline='') as csvfile:
	# set the reader to comma separated values
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	# iterate over each row in the csv file and store the data in our datastructures
	for row in csvreader:
		id = row[0]
		name = row[1]
		price = row[2]
		category = row[3]
		# add the product to the product hashmap so we can look up the product information 
		# based on product ID in O(1) time
		products[id] = {"name" : name, "price" : price, "category" : category}
		# add the product to the trie so we can look up matches based on a prefix 
		# in better than O(n) time
		trie[id] = (id, name, price)

# now start an indefinite loop to process user input data. We will break out of the loop
# either when the user quits or when they reach the end of selecting products, ringing them
# up, paying and outputting a receipt
while True:
	print()
	print("Please enter a product identifier or type 'h' for help: ")
	print()

	# get the input from the user
	userInput = input()
	print()

	if userInput == "h" or userInput == "help":
		print("Use the following commands:")
		print()
		print("%-15s %-40s" %("Command", "Description"))
		print("%-15s %-40s" %("help", "List the different commands"))
		print("%-15s %-40s" %("quit", "Quit the program"))
		print("%-15s %-40s" %("rungup", "List the rung up items"))
		print("%-15s %-40s" %("total", "Calculate the total bill and finish"))
		continue

	# functionality to total up and calculate taxes
	if userInput == "t" or userInput == "total":
		print("%-18s %-9s" %("Product name", "Price"))	
		total = 0 # the total amount
		totalCountyTaxable = 0 # the amount taxable by the county
		for r in rungup:	
			total += float(products[r]["price"]) # add up the total amounts, need to cast the price to a float
			# as the price is a decimal value
			if products[r]["category"] != "g":
				totalCountyTaxable += float(products[r]["price"]) # only add non grocery items to 
				# the county taxable amount
		print()
		print("%-18s %-9s" %("Subtotal: ", total))
		# add up the tax, 6.3% state + 2% city (8.3%) 
		# on everything, and 0.7% county on non grocery items. Round to 2 decimal places, dollars and cents		
		statetax = round(total*0.063, 2)
		countytax = round(totalCountyTaxable*0.007, 2)
		citytax = round(total*0.02, 2)
		tax = round(statetax + countytax + citytax, 2)
		print("%-18s %-9s" %("Tax: ", tax))
		print("%-18s %-9s" %("Total due: ", round(tax + total, 2)))
		print()

		# get the amount paid by the customer
		print("Please enter the amount paid by the customer:")
		customerAmount = float(input())
		print()
		print("Receipt:")
		print()
		print("%-18s %-18s %-10s %-17s" %("Product name", "Product identifier", "Price", "Tax category"))	

		for id in rungup:	
			print("%-18s %-18s %-10s %-17s" %(products[id]["name"], id, products[id]["price"], products[id]["category"]))	
		print()
		# print out the subtotal and taxes
		print("%-18s %-9s" %("Subtotal: ", total))
		print("%-18s %-9s" %("State tax: ", statetax))
		print("%-18s %-9s" %("County tax: ", countytax))	
		print("%-18s %-9s" %("City tax: ", citytax))	
		# print the total amount due, the amount paid by the customer, and the amount of change
		print("%-18s %-9s" %("Total due: ", round(tax + total, 2)))
		print("%-18s %-9s" %("Amount paid: ", customerAmount))
		change = customerAmount - tax - total
		print("%-18s %-9s" %("Change: ", round(change, 2)))
		print()
		print("Thank you! Have a nice day!")
		break

	# exit the program functionality
	if userInput == "q" or userInput == "quit" or userInput == "exit":
		break

	# functionlity to list the rung up items. Not in the problem set but useful to see
	# what has been rung up so far
	if userInput == "r" or userInput == "rungup":
		print("Rung up items so far: ")
		print()
		print("%-18s %-9s" %("Product name", "Price"))	
		# iterate through all the rung up items and print them out
		for r in rungup:	
			print("%-18s %-9s" %(products[r]["name"], products[r]["price"]))		
		continue

	# matching values
	matches = trie.values(userInput)

	# case where nothing matched
	if len(matches) == 0:
		print("No matches")
	# case where exactly one item matched
	elif len(matches) == 1:
		print("Ringing up: ")
		print()
		print("%-18s %-9s" %("Product name", "Price"))		
		# get the item and the relevant fields
		item = matches[0]
		id = item[0]
		name = item[1]
		price = item[2]
		print("%-18s %-9s" %(name, price)) # print the name and price our
		rungup.add(id) # add the product ID to the set of rung up items
	# case where multiple products match
	else:
		print("Mutiple matching products found: ")
		print()		
		print("%-15s %-20s" %("Product ID", "Product name"))
		for item in matches:
			id = item[0]
			name = item[1]
			print("%-15s %-20s" %(id, name))

		

		


