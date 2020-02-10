#!/usr/bin/env python3

import csv # used to read csv files 
from pytrie import StringTrie # used to match prefixes in better than O(n) time.
# O(n) time would be the case if we did not use a trie and instead naively looked
#  through all the n strings and check one by one
import locale # used for formatting the currency in prices

products = dict() # a dict is a hashmap representing the products, allows O(1) lookup of product price 
# informaton based on the product id

rungup = set() # this stores the products that we have rung up and allows O(1) insertion time

trie=StringTrie() # a trie that allows us to look up all the strings matching a
# prefix in faster than O(n) time where n is the number of strings

# set the locate for currency formatting
locale.setlocale( locale.LC_ALL, '' )

# first we will get the csv file name from the user
print("Please enter the csv product data filename or press ENTER to use the default (productdata.csv)")
filename = input()
if len(filename) == 0:
	filename = 'productdata.csv'

# use a try block in case opening the csv file fails
try:
	# when to program starts it reads the product data from the productdata.csv file
	with open(filename, newline='') as csvfile:
		# set the reader to comma separated values
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		# iterate over each row in the csv file and store the data in our datastructures
		for row in csvreader:
			# get the values out of each row
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
except:
	# if opening the file fails or the file does not exist, print an error message and exit
	print("Failed to open the csv file, exiting...")
	quit()

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

	# handle the user asking to exit the program
	if userInput == "q" or userInput == "quit" or userInput == "exit":
		break

	# handle the user asking for help
	if userInput == "h" or userInput == "help":
		print("Use the following commands:")
		print()
		print("%-15s %-40s" %("Command", "Description"))
		print("%-15s %-40s" %("help", "List the different commands"))
		print("%-15s %-40s" %("quit", "Quit the program"))
		print("%-15s %-40s" %("rungup", "List the rung up items"))
		print("%-15s %-40s" %("total", "Calculate the total bill and finish"))
		continue

	# functionlity to list the rung up items. Not in the problem set but useful to see
	# what has been rung up so far
	if userInput == "r" or userInput == "rungup":
		print("Rung up items so far: ")
		print()
		print("%-18s %9s" %("Product name", "Price"))	
		# iterate through all the rung up items and print them out
		for r in rungup:	
			print("%-18s %9s" %(products[r]["name"], locale.currency(float(products[r]["price"]))))		
		continue

	# functionality to total up and calculate taxes
	if userInput == "t" or userInput == "total":
		# do not compute the total if no items have been added, instead tell
		# the user to add some items
		if len(rungup) == 0:
			print("Please ring up some items before calculating the total")
			continue

		# print out the product names and prices, as required
		print("%-18s %9s" %("Product name", "Price"))	
		total = 0 # the total amount
		totalCountyTaxable = 0 # the amount taxable by the county
		# iterate over each of the rung up items 
		for r in rungup:	
			total += float(products[r]["price"]) # add up the total amounts, need to cast the price to a float
			# as the price is a decimal value
			if products[r]["category"] != "g":
				totalCountyTaxable += float(products[r]["price"]) # only add non grocery items to 
				# the county taxable amount
		print()
		print("%-18s %9s" %("Subtotal: ", locale.currency(total)))
		# add up the tax, 6.3% state + 2% city (8.3%) 
		# on everything, and 0.7% county on non grocery items. Round to 2 decimal places, dollars and cents		
		statetax = round(total*0.063, 2)
		countytax = round(totalCountyTaxable*0.007, 2)
		citytax = round(total*0.02, 2)
		tax = round(statetax + countytax + citytax, 2)
		print("%-18s %9s" %("Tax: ", locale.currency(tax)))
		print("%-18s %9s" %("Total due: ", locale.currency(round(tax + total, 2))))
		print()

		# get the amount paid by the customer
		customerAmount = -1
		while customerAmount < round(tax + total, 2):
			print("Please enter the amount paid by the customer:")
			inputFromUser = input()
			# use a try catch block to handle the user entering text instead of a number
			try:
				customerAmount = float(inputFromUser)	
			except:
				print("Please enter a numerical value")
			if customerAmount < round(tax + total, 2):
				print("The amount paid by the customer must not be less than the amount due")
		print()
		# now print out the receipt
		print("Receipt:")
		print()
		# print the column headings
		print("%-18s %-18s %10s %-17s" %("Product name", "Product identifier", "Price", "Tax category"))	
		# print out each of the rung up products
		for id in rungup:	
			print("%-18s %-18s %10s %-17s" %(products[id]["name"], id, locale.currency(float(products[id]["price"])), products[id]["category"]))	
		print()
		# print out the subtotal and taxes, formatting as a currency (dollar amount)
		print("%-18s %9s" %("Subtotal: ", locale.currency(total)))
		print("%-18s %9s" %("State tax: ", locale.currency(statetax)))
		print("%-18s %9s" %("County tax: ", locale.currency(countytax)))	
		print("%-18s %9s" %("City tax: ", locale.currency(citytax)))	
		# print the total amount due, the amount paid by the customer, and the amount of change
		print("%-18s %9s" %("Total due: ", locale.currency(round(tax + total, 2))))
		print("%-18s %9s" %("Amount paid: ", locale.currency(customerAmount)))
		change = customerAmount - tax - total
		print("%-18s %9s" %("Change: ", locale.currency(round(change, 2))))
		print()
		# print a goodbye message
		print("Thank you! Have a nice day!")
		# break to ensure that we exit the while loop and the program completes and exits
		break

	# prefix matching values from the trie - trie provides faster than O(n) prefix matching against n strings
	matches = trie.values(userInput)

	# case where nothing matched
	if len(matches) == 0:
		print("No matches")
	# case where exactly one item matched
	elif len(matches) == 1:	
		# get the item and the relevant fields
		item = matches[0]
		id = item[0]
		name = item[1]
		price = item[2]
		# if an item has already been rung up then print a message and continue
		if id in rungup:
			print("That item has already been rung up")
			continue
		# ring up that one item
		print("Ringing up: ")
		print()
		print("%-18s %9s" %("Product name", "Price"))	

		print("%-18s %9s" %(name, locale.currency(float(price)))) # print the name and price our
		rungup.add(id) # add the product ID to the set of rung up items
	# case where multiple products match
	else:
		# if multiple products match the prefix then print them out but do not ring them up
		print("Mutiple matching products found: ")
		print()	
		# print out the matching products	
		print("%-15s %-20s" %("Product ID", "Product name"))
		for item in matches:
			id = item[0]
			name = item[1]
			print("%-15s %-20s" %(id, name))

		

		


