#! /usr/bin/python

# vim: set ai sw=4 et:

import random
import time
import copy

# The main class for a gift exchange
class GiftExchange(object):
    """Class GiftExchange
       A GiftExchange takes a set of participants and arranges them into
       giver/receiver pairs so that every participant is a giver and a
       receiver exactly once.
       In addition, this has a concept of families.  Each participant is
       a member of a family and may not give to or receive from a member
       of his or her family (or to/from him/herself).

       The class starts off having no participants.  Then, to initialize the
       exchange, families are added one at a time using the add_family()
       method.  A family is just a list of names.

       There are 2 methods for generating a complete exchange:
       1) generate_exchange().  This method uses constraint propagation and
          searching to generate the giver/receiver pairs.  If no pairing
          of names meets the criteria, this method will return False;
          otherwise it will return true, and the self.recips variable will
          have a dictionary mapping givers (key) to recipients (value).
       2) generate_pairing().  This method is much less sophisticated.
          It simply generates random permutations of all the participants'
          names until one of the pairings meets the constraints.  If no
          pairing of names matches the criteria, this method will continue
          trying forever.

       A gift exchange will reject addition of a family if any of the names
       in that family are duplicates (either of existing names in the exchange
       or of another name in the same family).
       
       Typical usage of the class looks like this:
           # Create a member of the class.
           ge = GiftExchange()
           # Add the participants, one family at at time.
           ge.add_family(['name1', 'name2', 'name3'])
           ge.add_family(['name4', 'name5'])
           ge.add_family(['name6', 'name7', 'name8'])
           ge.add_family(['name9', 'name10', 'name11', 'name12'])
           # Create the mapping.
           ge.generate_exchange()
           # Show everything about the class (including the exchange)
           ge.show()

        Class Methods:
            __init__(self):
                Initialize the class instance variables.
            show(self):     
                Print the class instance variables in a nice format
            add_family(self, family):
                Add a family to the exchange.
                A family is a list of names.
            assign(self, giver, recip):
                Assign the recipient to the giver in the exchange.
            eliminate(self, giver, recip):
                Remove the recipient from the giver's list of possible
                recipients in the exchange.
            reset_exchange(self):
                Reset the recips dictionary to its initial state.
                This means that each giver's list of possible recipients is
                everyone not in that giver's family.
            generate_exchange(self):
                Given an initialized recips dictionary, generate a random
                exchange with each participant giving to and receiving from
                a single other participant.
                This routine can be called multiple times, but will only
                generate a new exchange if the exchange is reset (via the
                reset_exchange() method), between calls.
            generate_pairing(self):
                Generates random permutations of the participants until one
                of them meets the constraints (no one gives to herself or
                to a family member).
                This routine can be called repeatedly, and will generate a new
                pairing each time.
            show_pairing(self):
                Show the exchange's current pairing.  If generate_pairing() has
                not been called, yet, then will show "None."

        Debugging:
            The show() method on the class shows all the current state.
            Setting the verbose variable to True will enable printing of
            debugging information for some methods (currently just
            generate_exchange()).
            An exchange can be reset to default state by calling the
            reset_exchange() method.
            Extra constraints on an exchange can be applied by calling the
            assign() and eliminate() methods directly."""

    def __init__(self):
        print "Initializing new GiftExchange."
        self.namelist = []
        self.family_list = []
        self.family_dict = {}
        self.num_families = 0
        self.pairing = None
        self.tries = 0
        self.recips = {}
        self.verbose = False

    def show(self):
        print "Exchange participants:"
        print "    %s" % ", ".join(self.namelist)

        print "Families (%d):" % self.num_families
        for (index,f) in enumerate(self.family_list):
            print "  %d: %s" % (index, ", ".join(f))

        print "Possible recipients:"
        for name in self.namelist:
            print "  %s: %s" % (name, self.recips[name])

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
        # Add each member of new family to the list of possible recipients
        # for everyeone already in the exchange.
        for giver in self.namelist:
            for recipient in family:
                self.recips[giver].append(recipient)
        # For each member of the new family, make the list of possible
        # recipients the same as the list of everyone already in the exchange.
        for giver in family:
            self.recips[giver] = list(self.namelist)

        # Add the new family to the family list.
        self.family_list.append(family)

        # Add each member of the new family to the lists.
        for name in family:
            self.namelist.append(name)
            self.family_dict[name] = self.num_families
        self.num_families += 1

    def assign(self, giver, recip):
        """Eliminate alll other recipients but the given one and propagate.
           return True if successful, False if there is a contradiction."""
        other_recips = [r for r in self.recips[giver] if r != recip]
        return all(self.eliminate(giver, r) for r in other_recips)

    def eliminate(self, giver, recip):
        if not recip in self.recips[giver]:
            return True
        self.recips[giver].remove(recip)
        if len(self.recips[giver]) == 0:
            return False
        elif len(self.recips[giver]) == 1:
            r2 = self.recips[giver][0]
            if not all (self.eliminate(g2, r2) for g2 in self.namelist if g2 != giver):
                return False

        poss_givers = [g for g in self.namelist if recip in self.recips[g]]
        if len(poss_givers) == 0:
            return False
        elif len(poss_givers) == 1:
            return self.assign(poss_givers[0], recip)
        return True

    def reset_exchange(self):
        for giver in self.namelist:
            self.recips[giver] = \
                [r for r in self.namelist if self.family_dict[giver] != self.family_dict[r]]

    def generate_exchange(self):
        """generate_exchange:
           Given the current set of possible giver->recipient combinations, search
           for a pairing.  This assumes that the primary constraints have already been
           applied (giver doesn't give to him/her self, giver doesn't give to a family
           member), so we just try to get a list where each giver has a single
           recipient, and each recipient has a single giver."""
           
        # Is the exchange already screwed up?
        if any(len(self.recips[g])==0 for g in self.namelist):
            return False
        # Is the exchange already solved?
        if all(len(self.recips[g])==1 for g in self.namelist):
            return True

        # Start making guesses.
        # Start with one of the givers who has the least number of possible recipients.
        #  (To exercise the code paths, change the below to max(...).
        #  I have never found a case that was possible to solve that wasn't solved on the
        #  first guess at each step when using min(...).
        n,g = min((len(self.recips[g]), g) for g in self.namelist if len(self.recips[g]) > 1)
        # saved_recips = self.recips.copy()
        saved_recips = copy.deepcopy(self.recips)
        rlist = saved_recips[g]
        random.shuffle(rlist)
        if self.verbose: print "  Going to try %s gives to %s" % (g,rlist)
        for r in rlist:
            # Always start from the same spot.
            # self.recips = saved_recips.copy()
            self.recips = copy.deepcopy(saved_recips)
            if self.verbose:
                print "  Trying %s gives to %s" % (g,r)
                if False:
                    for name in self.namelist:
                        print "  %s: %s" % (name, self.recips[name])
            if not self.assign(g,r):
                # if self.verbose: print "  Done trying %s gives to %s" % (g,r)
                continue
            if self.generate_exchange():
                # if self.verbose: print "  Trying %s gives to %s succeeded." % (g,r)
                return True
            # if self.verbose: print "  Done trying %s gives to %s (next)" % (g,r)
        return False

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
