# cashregister
Cash Register App

The cashregister.py file contains my program for the cash register problem.
To run the file use the command: ./cashregister.py
Make sure that the productdata.csv file is in the same directory as cashregister.py when you run it.

Choice of data structures:

I used three main data structures to store the product information to allow for efficient lookup of data:
1) Set - I stored the rung up items in a set. This allows constant time insertion and ensures that we don't add duplicates
2) Hashmap - I stored the product information in a hashmap (a "dict" in python). This maps from product ID to 
another hashmap with the other product information. This allows for the lookup of product name, price and tax 
category in constant time based on a product ID.
3) Trie - I stored the product IDs in a trie. A trie allows for efficient matching of prefixes against strings.
This allows us to efficiently look up the strings that match a prefix, without having to read through the strings
that don't match the prefix.

Additional functions:
In addition to the functions in the problem set, I also implemented the following:
1) Help function - this allows the user to type "help" and see a list of all the possible commands
2) Rungup function - this allows the user to type "rungup" to see which items they have rung up so far
