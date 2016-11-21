# NOTE: This was used to ease transition for python to c++ for the new iterative algo.
# However, the iterative algo is now more fleshed out on the c++ version, so this code is old.

import sys
import time
import random

from joblib import Parallel, delayed
import multiprocessing


# Declare global variables that functions can access, if they need them (this way, we don't have to pass them as args)
a = None                    # the line representation, which is a string on the alphabet, {H, G, W, T}
opt_pairs_table = None      # table for storing memoized outputs of OPT for all i and j pairs

def OPT_iter(i, j):
    global a

    for col in range(len(a)):
        # opt_ret = Parallel(n_jobs=4)(delayed(OPT)(row, row+col) for row in range(len(a) - col))
        for row in range(len(a) - col):
            opt_ret = OPT(row, row+col)

    return opt_ret

def OPT(i, j, in_call=False):
    global a, opt_pairs_table

    if i < 0 or j < 0 or i > len(a) - 1 or j > len(a) - 1:
        return 0

    # Use memoized result, if available
    if opt_pairs_table[i][j] != -1:
        return opt_pairs_table[i][j]

    # To avoid sharp turns, we don't look for pairs when i and j are less than or equal to 4 spaces away from each other
    if i >= (j-4):
        opt_pairs_table[i][j] = 0
        return 0

    if in_call:
        print "REALLY BAD", i, j

    # Set the max optimal number of pairs to OPT(i, j-1), in case no optimal t is found that beats it
    max_opt = OPT(i, j-1)

    # Look for optimal pairing for a[j] (which we call a[t]), by going through all possible t's
    for t in range(i, j-4):
        # check if valid pairing
        if a[t] + a[j] in ["HG", "GH", "WT", "TW"]:
            # recursively call OPT for the line before t, for the line after t, and add 1 to account for a[t] itself
            opt = (OPT(i, t-1, in_call=True)) + (OPT(t+1, j-1, in_call=True)) + 1
            # if the optimal number of pairs for this choice of t is larger than max_opt, make it max_opt
            if opt >= max_opt:
                max_opt = opt

    # Memoize this result so we don't have to recompute it again, then return it
    opt_pairs_table[i][j] = max_opt
    return max_opt

def get_random_line(n):
    return ''.join(random.choice("HGWT") for _ in xrange(n))


def get_line_from_file(file_name, n):
    return open(file_name).readline()[:n]

def main():
    global a, opt_pairs_table
    # Initialize the line representation, a, which is a string on the alphabet, {H, G, W, T}
    # a = "HGGTHWHWWHTG"

    line_length = 500
    # a = get_random_line(n=line_length)
    a = get_line_from_file("test_data.txt", n=line_length)

    n = len(a)
    # python's recursion depth limit is 1000, so increase it if we need to
    if n > 1000:
        sys.setrecursionlimit(n)

    # Initialize a n-by-n 2D array of -1s, for storing memoized outputs of OPT for all i and j pairs
    # This is done in theta(n^2) time
    opt_pairs_table = [[-1 for col in range(n)] for row in range(n)]
    # for i in range(n):
    #     for j in range(n):
    #         if i >= (j-4):
    #             opt_pairs_table[i][j] = 0

    # Calculate the optimal pairs for whole line, which will make recursive calls to subproblems
    start_time = time.time()
    opt_num_pairs = OPT_iter(0, n - 1)
    end_time = time.time()
    print "n = " + str(n) + ", OPT(1, n) = " + str(opt_num_pairs),
    print "(Done in", end_time - start_time, "seconds)"

    return 0

if __name__ == '__main__':
    main()