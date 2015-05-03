# The original obfuscated one-liner.
# Comment: primes < 1000

# print filter(None,map(lambda y:y*reduce(lambda x,y:x*y!=0, map(lambda x,y=y:y%x,range(2,int(pow(y,0.5)+1))),1),range(2,1000)))

# Let's expand it
# Just make it separate lines.
plist1 = filter(None,
               map(lambda y:y*reduce(lambda x,y:x*y!=0,
                                     map(lambda x,y=y:y%x,
                                         range(2,int(pow(y,0.5)+1)))
                                     ,1),
                   range(2,1000)))
# print plist1

#
# Break pieces of the job into functions.
#
def mappy(y):
    """For any number, returns a list of remainders when that number is devided by each integer
     from 2 up to its square root."""
    return map(lambda x,y=y:y%x,range(2,int(pow(y,0.5)+1)))

def reducey_old(i):
    """For the number, convert the remainders into a truth function.
       If any remainder is 0, then the number is not prime, so return false."""
    return reduce(lambda x,y: x**y!=0, mappy(i), 1)

def reducey(i):
    """For the number, convert the remainders into a truth function.
       If any remainder is 0, then the number is not prime, so return false.
       Note use of "y and " instead of "x and y" which keeps the lambda function
       returning True (1) or False (0), even if a remainder was large than 1."""
    return reduce(lambda x,y: y and x, mappy(i), True)


def listy(i):
    return map(lambda y: y*reducey(y), range(2,i))
# For each integer, put either 0 or that integer in a list, depending
# on whether it is prime or not.
intlist = map(lambda y: y*reducey(y), range(2,1000))

# Reduce the above list to just the primes.
plist2 = filter(None, intlist)

print plist2
