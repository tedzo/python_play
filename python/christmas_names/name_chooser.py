#! /usr/bin/python

# vim: set ai sw=4:

import random
import time

# The main class for a gift exchange
class GiftExchange(object):
    def __init__(self):
        print "Initializing new GiftExchange."
        self.namelist = []
        self.family_list = []
        self.family_dict = {}
        self.num_families = 0
        self.pairing = None
        self.tries = 0

    def show(self):
        print "Exchange participants:"
        print "    %s" % ", ".join(self.namelist)

        print "Families (%d):" % self.num_families
        for (index,f) in enumerate(self.family_list):
            print "  %d: %s" % (index, ", ".join(f))

	if self.pairing:
	    print "Here is the exchange:"
	    self.show_pairing()
	    print "Pairing took %d tries." % self.tries

    def add_family(self, family):
        # Do a bit of sanity checking on the input before adding the family.
        if len(family) == 0:
            # throw exception
            print "Ignoring empty family input list."
            return
        for name in family:
            if name in self.namelist:
                # throw exception
                print "Ignoring new family with duplicate name: %s." % name
		return
        self.family_list.append(family)
        for name in family:
            self.namelist.append(name)
            self.family_dict[name] = self.num_families
        self.num_families += 1

    # Create random pairings (just permutations of the name list), until one of them
    # meets the necessary criteria.
    # Current criteria are:
    #    - No one gives to a family member
    #    - No one gives to herself.  (Which is taken care of by the above.)
    def generate_pairing(self):
        def is_good(pairing):
            for (giver, recipient) in pairing:
                if self.family_dict[giver] == self.family_dict[recipient]:
                    return False
            return(True)
        def gen_random_pairing(giver_list):
            # Copy the list, randomize (permute) the copy, and make the pairs.
            recipient_list = list(giver_list)
            random.shuffle(recipient_list)
            return zip(giver_list, recipient_list)

        tries = 0
        pairing = gen_random_pairing(self.namelist)
        while not is_good(pairing):
            pairing = gen_random_pairing(self.namelist)
            tries += 1

        self.pairing = pairing
        self.tries = tries

    # Print a pairing nicely.
    def show_pairing(self):
        if self.pairing == None:
            print "%8s" % "None"
            return
        for p in self.pairing:
            print "%8s gives to %s." % p

if __name__ == "__main__":
    # Edit this list to set the participants in the exchange.
    family_list = [["Alia", "Tanya"],
		   ["Nick", "Ariana", "Max"],
		   ["Paige", "Ian", "Kendra"]
		  ]
    ge = GiftExchange()
    for f in family_list:
        ge.add_family(f)
    ge.show()
    ge.generate_pairing()
    ge.show()
