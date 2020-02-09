#!/usr/bin/env python3



import csv

products = dict() # dict representing the products

# when to program starts it reads the product data from the productdata.csv file
with open('productdata.csv', newline='') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in csvreader:
		id = row[0]
		name = row[1]
		price = row[2]
		category = row[3]
		products[id] = {"name" : name, "price" : price, "category" : category}
		
print(products)
		


