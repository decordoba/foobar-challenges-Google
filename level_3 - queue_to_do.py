"""
Queue To Do
===========

You're almost ready to make your move to destroy the LAMBCHOP doomsday device, but the security checkpoints that guard the underlying systems of the LAMBCHOP are going to be a problem. You were able to take one down without tripping any alarms, which is great! Except that as Commander Lambda's assistant, you've learned that the checkpoints are about to come under automated review, which means that your sabotage will be discovered and your cover blown - unless you can trick the automated review system.

To trick the system, you'll need to write a program to return the same security checksum that the guards would have after they would have checked all the workers through. Fortunately, Commander Lambda's desire for efficiency won't allow for hours-long lines, so the checkpoint guards have found ways to quicken the pass-through rate. Instead of checking each and every worker coming through, the guards instead go over everyone in line while noting their security IDs, then allow the line to fill back up. Once they've done that they go over the line again, this time leaving off the last worker. They continue doing this, leaving off one more worker from the line each time but recording the security IDs of those they do check, until they skip the entire line, at which point they XOR the IDs of all the workers they noted into a checksum and then take off for lunch. Fortunately, the workers' orderly nature causes them to always line up in numerical order without any gaps.

For example, if the first worker in line has ID 0 and the security checkpoint line holds three workers, the process would look like this:
0 1 2 /
3 4 / 5
6 / 7 8
where the guards' XOR (^) checksum is 0^1^2^3^4^6 == 2.

Likewise, if the first worker has ID 17 and the checkpoint holds four workers, the process would look like:
17 18 19 20 /
21 22 23 / 24
25 26 / 27 28
29 / 30 31 32
which produces the checksum 17^18^19^20^21^22^23^25^26^29 == 14.

All worker IDs (including the first worker) are between 0 and 2000000000 inclusive, and the checkpoint line will always be at least 1 worker long.

With this information, write a function answer(start, length) that will cover for the missing security checkpoint by outputting the same checksum the guards would normally submit before lunch. You have just enough time to find out the ID of the first worker to be checked (start) and the length of the line (length) before the automatic review occurs, so your program must generate the proper checksum with just those two values.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) start = 0
    (int) length = 3
Output:
    (int) 2

Inputs:
    (int) start = 17
    (int) length = 4
Output:
    (int) 14
"""

def answer(start, length):
    """
    We only have to XOR the numbers to the left of the / in the
    example below. Therefore, we can see that in every row, the first
    number is start + row*length, and each row has exactly
    length - row numbers. In the example below, start=17, length=4,
    21=17+4, 25=17+2*4, 29=17+3*4...
    This function calculates every row separately, and XOR's each
    row with the next one, to obtain the XOR of all rows.
    Example: answer(17, 4)
    17 18 19 20 /
    21 22 23 / 24
    25 26 / 27 28
    29 / 30 31 32
    The answer should be 17^18^19^20^21^22^23^25^26^29
    """
    checksum = 0
    for row in range(length):
        checksum = calculateRow(start + row*length,
                                length - row, checksum)
    return checksum


def calculateRow(start, length, prev_id=0):
    """
    Given the first number of the row, the number of positions in the
    row, and the previous checksum (XOR), performs the XOR in all the
    elements in the queue.
    To solve the XOR fast without iterating over every number, we
    solve XOR bitwise, and therefore, for each row we do at most 31
    calls, considering that 2000000000 is the greatest possible number.
    Therefore, the complexity is O(log(start+length))
    Example: calculateRow(3, 4, 0) does 0^3^4^5^6 = 4 (where ^ = XOR)
    """
    current_id = prev_id
    end = start + length
    # We calculate from LSB to MSB. e.g. for 32 we compute bits 0 to 5
    for i in range(end .bit_length()):
        # The LSB is a special case, so we compute it differently
        # Here, we get the mod of the length by 4, and depending on
        # this number and the first bit (0 or 1) we apply XOR or not
        if i == 0:
            relevant_bits = length % 4
            first_bit = start & 1
            if ((relevant_bits == 1 and first_bit) or
                    (relevant_bits == 2) or
                    (relevant_bits == 3 and not first_bit)):
                current_id ^= 1
        # We use computeXOROfBit to calculate the XOR for every bit
        # The trick is that, because the numbers are ordered, we can
        # discard chunks of numbers of fixed size with XOR=0
        # e.g. 00001111 will give XOR=0, even if ordered 00011110
        else:
            # We only need to XOR the first relevant_bits, the rest have XOR=0
            relevant_bits = length % (2**(i + 1))
            current_id ^= computeXOROfBit(start, relevant_bits, i)
    return current_id


def computeXOROfBit(start, length, bit_position):
    """
    Returns the XOR of bit_position between the numbers start and
    start + length. It does this by counting the 1s, and if it gets
    an even number the XOR is 0, if not it is 1.
    To count the number of 1s in bit_position between the numbers 
    start and start + length, we find the first 1 of the sequence
    and the last 1, and do some operations to find the exact amount
    without iterating through all the numbers.
    Example: computeXOROfBit(2, 5, 2) does (2^3^4^5^6)&4 = 4
    This function only works if length < 2^bit_position
    """
    # Calculate the position of the end (we will count 1s from start to end-1)
    end = start + length
    # Create a mask for our bit_position
    mask = 1 << bit_position
    # Find where the zeros would start before our number
    prev_zero = start - (start % (mask * 2))
    # Find the first one in our sequence. It can be in start or afterwards
    first_one = max(start, prev_zero + mask)
    # If we don't see any one, we return 0 
    if first_one > end:
        return 0
    # Find the position where the stream of ones ends. It can be in end or before
    end_ones = min(end, prev_zero + 2 * mask)
    # Count the number of ones
    num_ones = end_ones - first_one
    # Check if there is another stream of ones in our sequence and add it
    next_ones = prev_zero + 3 * mask
    if end > end_ones + mask:
        num_ones += end - next_ones
    # Return the XOR of bit_position and put it in its position
    return mask * (num_ones % 2)


def calculateRowSlow(start, length, prev_id=0):
    """
    Given the first number of the row, the number of positions in the
    row, and the previous checksum (XOR), performs the XOR in all the
    elements in the queue.
    Example: calculateRow(3, 4, 0) does 0^3^4^5^6 = 4 (where ^ = XOR)

    This code is too slow, as it will take O(length) time. For a
    faster implementation, check calculateRow

    Still, it can be tried out by substituting calculateRow by
    calculateRowSlow in line 66
    """
    current_id = prev_id
    for n in range(start, start + length):
        current_id ^= n
    return current_id