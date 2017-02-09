"""
Find the Access Codes
=====================

In order to destroy Commander Lambda's LAMBCHOP doomsday device, you'll need access to it. But the only door leading to the LAMBCHOP chamber is secured with a unique lock system whose number of passcodes changes daily. Commander Lambda gets a report every day that includes the locks' access codes, but only she knows how to figure out which of several lists contains the access codes. You need to find a way to determine which list contains the access codes once you're ready to go in.

Fortunately, now that you're Commander Lambda's personal assistant, she's confided to you that she made all the access codes "lucky triples" in order to help her better find them in the lists. A "lucky triple" is a tuple (x, y, z) where x divides y and y divides z, such as (1, 2, 4). With that information, you can figure out which list contains the number of access codes that matches the number of locks on the door when you're ready to go in (for example, if there's 5 passcodes, you'd need to find a list with 5 "lucky triple" access codes).

Write a function answer(l) that takes a list of positive integers l and counts the number of "lucky triples" of (lst[i], lst[j], lst[k]) where i < j < k.  The length of l is between 2 and 2000 inclusive.  The elements of l are between 1 and 999999 inclusive.  The answer fits within a signed 32-bit integer. Some of the lists are purposely generated without any access codes to throw off spies, so if no triples are found, return 0.

For example, [1, 2, 3, 4, 5, 6] has the triples: [1, 2, 4], [1, 2, 6], [1, 3, 6], making the answer 3 total.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int list) l = [1, 1, 1]
Output:
    (int) 1

Inputs:
    (int list) l = [1, 2, 3, 4, 5, 6]
Output:
    (int) 3
"""

def answer(l):
    """
    To reduce time complexity, we check for pairs that divide each other
    (O(n^2)) and record the results. Then, we check for pairs again, and
    add the number of pairs of the smaller element when we find one.
    """
    pairs = []
    # Record the number of divisor pairs (l[k], l[j]) for every element
    # in l, where k<j and l[j]%l[k]==0
    for j in range(len(l)):
        num_pairs = 0
        for k in range(j):
            if l[j] % l[k] == 0:
                num_pairs += 1
        pairs.append(num_pairs)
    # Search l for pairs (l[j], l[i]) again for every element in l, where
    # j<i and l[i]%l[j]==0, and add to num_triples the number of pairs of
    # the smaller element j for every pair (l[j], l[i]) we find
    num_triples = 0
    for i in range(len(l)):
        for j in range(i):
            if l[i] % l[j] == 0:
                num_triples += pairs[j]
    return num_triples


def answerSlow(l):
    """
    This is a version of the answer with O(n^3) time complexity, which
    is too slow, and O(1)space complexity. See answer(l) for a faster
    implementation with O(n^2) time complexity and O(n) space complexity.
    """
    num_triples = 0
    for i in range(len(l)):
        for j in range(i):
            # If l[j] does not divide l[i], don't look for l[j] divisors
            if l[i] % l[j] != 0:
                continue
            for k in range(j):
                if l[j] % l[k] == 0:
                    # If l[i]%l[j]==0 and l[j]%l[k]==0, new_triple
                    num_triples += 1
    return num_triples