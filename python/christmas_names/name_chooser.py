#! /usr/bin/python

# vim: set ai sw=4:

import random
import time

family_list = [["Alia", "Tanya"],
	       ["Nick", "Ariana", "Max"],
	       ["Paige", "Ian", "Kendra"]
	      ]

# Given a family_list, create 2 new data structures:
#   1) Just a raw list of all the names
#   2) A dictionary mapping from a name to a family identifier
family_dict = {}
namelist = []

family_id = 0
for family in family_list:
    for name in family:
	family_dict[name] = family_id
	namelist.append(name)
    family_id += 1

# Create a random pairing (really just a permutation of the input list).
# This is returned as a list of pairs of names.
def pairing(input):
    leftlist = list(input)
    rightlist = list(input)

    random.shuffle(rightlist)
    return zip(leftlist, rightlist)

# Print a pairing nicely.
def show_pairing(pairing):
    for p in pairing:
	print "%8s gives to %s." % p

# Apply the constraints to a pairing.  If it meets the constraints,
# return True; otherwise, return False.
def pairing_good(pairing):
    for p in pairing:
	if p[0] == p[1]: return False
	if family_dict[p[0]] == family_dict[p[1]]: return False
    return(True)

# Keep creating pairings until we find a good one.
def find_good_pairing(return_num_tries=False):
    num_tries = 0
    while (True):
	p = pairing(namelist)
	num_tries +=1
	# print "Trying pairing", show_pairing(p)
	if pairing_good(p):
	    print ("Took %d tries to get a good pairing." % num_tries)
	    if return_num_tries:
		return (p, num_tries)
	    else:
		return p
	# time.sleep(1)
