#! /usr/bin/env python

# vim: set ai sw=4 sm:

import os
import sys
import argparse

def parallel(*resistors):
    """Calculate an equivalent resistory value for parallel resistors.
    
    Given resistor values as input, assume they are put in parallel in a circuit, and
    return the equivalent resistor value as if they were a single resistor.
    """
    
    # Each parallel resistor allows a certain amount of current through (v/r)
    # The total current through all parallel resistors is the sum of each of the currents.
    # The final equivalent resistance is the voltage divided by the total current.
    # r = v / ( (v/r1) + (v/r2) + ...)
    #   = v / (v (1/r1) + (1/r2) + ...)
    #   = 1 / (1/r1 + 1/r2 + ...)
    current = 0
    for r in resistors:
	current += 1.0 / r
    if current == 0:
	return 1.0	# Whatever.  No inputs; just return 1.
    else:
	return 1.0 / current

def series(*resistors):
    """Calculate an equivalent resistory value for series resistors.
    
    Given resistor values as input, assume they are put in series in a circuit, and
    return the equivalent resistor value as if they were a single resistor.
    """
    return sum(resistors)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('resistors', metavar='R', type=float, nargs='+')
    args = p.parse_args()
    # print args
    print parallel(*args.resistors)
