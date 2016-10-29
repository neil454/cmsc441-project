import sys
import time
import random

# Declare global variables that functions can access, if they need them (this way, we don't have to pass them as args)
a = None                    # the line representation, which is a string on the alphabet, {H, G, W, T}
opt_pairs_table = None      # table for storing memoized outputs of OPT for all i and j pairs
opt_choices_table = None    # table for storing the optimal choices of each iteration (for recomputing S later)
S = None                    # actual solution (optimal pairs themselves), to be recomputed later

# TODO add comments about time complexity of certain code blocks?
def OPT(i, j):
    global a, opt_pairs_table, opt_choices_table

    # Use memoized result, if available
    if opt_pairs_table[i][j] != -1:
        return opt_pairs_table[i][j]

    # To avoid sharp turns, we don't look for pairs when i and j are less than or equal to 4 spaces away from each other
    if i >= (j-4):
        opt_pairs_table[i][j] = 0
        return 0

    # Set the max optimal number of pairs to OPT(i, j-1), in case no optimal t is found that beats it
    max_opt = OPT(i, j-1)
    # Set the optimal choice as if optimal t is not found (if it is, this will be overwritten below)
    opt_choices_table[i][j] = 0

    # Look for optimal pairing for a[j] (which we call a[t]), by going through all possible t's
    for t in range(i, j-4):
        # check if valid pairing
        if a[t] + a[j] in ["HG", "GH", "WT", "TW"]:
            # recursively call OPT for the line before t, for the line after t, and add 1 to account for a[t] itself
            opt = (OPT(i, t-1)) + (OPT(t+1, j-1)) + 1
            # if the optimal number of pairs for this choice of t is larger than max_opt, make it max_opt
            if opt >= max_opt:
                max_opt = opt
                # Also set the optimal choice to this pairing of a[t] and a[j], since it is currently the best
                opt_choices_table[i][j] = (t, j)

    # Memoize this result so we don't have to recompute it again, then return it
    opt_pairs_table[i][j] = max_opt
    return max_opt


def reconstruct_S(i, j):
    global a, S, opt_choices_table

    # if the current position is at a -1, or it's out of bounds, return out of the recursive call
    if opt_choices_table[i][j] == -1 or i < 0 or j < 0 or i > len(a)-1 or j > len(a)-1:
        return
    # if the current position is at a 0, that means there is no optimal pairing for j here, so go to j-1
    elif opt_choices_table[i][j] == 0:
        reconstruct_S(i, j-1)
    # otherwise, we have an optimal pairing
    else:
        # store the pairing in S
        S.append(opt_choices_table[i][j])
        # move on to next pairing, by checking the table for best optimal pairing before t, and after t
        reconstruct_S(i, opt_choices_table[i][j][0] - 1)
        reconstruct_S(opt_choices_table[i][j][0] + 1, opt_choices_table[i][j][1] - 1)

def get_random_line(n):
    return ''.join(random.choice("HGWT") for _ in xrange(n))

def get_line_from_file(file_name, n):
    return open(file_name).readline()[:n]

def main():
    global a, opt_pairs_table, opt_choices_table, S
    # Initialize the line representation, a, which is a string on the alphabet, {H, G, W, T}
    # a = "HGGTHWHWWHTG"

    line_length = 100
    # a = get_random_line(n=line_length)
    a = get_line_from_file("test_data.txt", n=line_length)

    n = len(a)
    # python's recursion depth limit is 1000, so increase it if we need to
    if n > 1000:
        sys.setrecursionlimit(n)

    # Initialize a n-by-n 2D array of -1s, for storing memoized outputs of OPT for all i and j pairs
    # This is done in theta(n^2) time
    opt_pairs_table = [[-1 for col in range(n)] for row in range(n)]

    # initialize a n-by-n 2D array of -1s, for storing the optimal choices of each iteration (for recomputing S later)
    # This is done in theta(n^2) time
    opt_choices_table = [[-1 for col in range(n)] for row in range(n)]

    # Calculate the optimal pairs for whole line, which will make recursive calls to subproblems
    start_time = time.time()
    opt_num_pairs = OPT(0, n - 1)
    end_time = time.time()
    print "n = " + str(n) + ", OPT(1, n) = " + str(opt_num_pairs),
    print "(Done in", end_time - start_time, "seconds)"

    # Recompute the actual solution (optimal pairs themselves), S
    S = []
    reconstruct_S(0, n-1)
    assert opt_num_pairs == len(S)
    print "S =", S

    return 0

if __name__ == '__main__':
    main()