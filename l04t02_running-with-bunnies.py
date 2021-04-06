'''
Running with Bunnies
====================

You and the bunny workers need to get out of this collapsing death trap of a space station -- and fast! Unfortunately, some of the bunnies have been weakened by their long work shifts and can't run very fast. Their friends are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can and get through the bulkheads before they close.

The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ..., last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave -- you can move to and from the bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact with the space station's security checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is traversed, the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to calculate the most bunnies you can pick up and which bunnies they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest worker IDs (as indexes) in sorted order. The bunnies are represented as a sorted list by worker ID, with the first bunny being 0. There are at most 5 bunnies, and time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point, bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best combination for this space station hallway, so the solution is [1, 2].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 1, 1, 1, 1}, {1, 0, 1, 1, 1}, {1, 1, 0, 1, 1}, {1, 1, 1, 0, 1}, {1, 1, 1, 1, 0}}, 3)
Output:
    [0, 1]

Input:
Solution.solution({{0, 2, 2, 2, -1}, {9, 0, 2, 2, -1}, {9, 3, 0, 2, -1}, {9, 3, 2, 0, -1}, {9, 3, 2, 2, 0}}, 1)
Output:
    [1, 2]

-- Python cases --
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output:
    [0, 1]
'''

# Implementation based on https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
# and augmented to track bunnies along the route.
# Modifies times in-place and returns a same-size matrix of bunnies found
def FloydWarshall(times):
    bunnies = [[set() for j in range(len(times))] for i in range(len(times))]
    for i in xrange(len(times)):
        for j in xrange(1, len(times)-1):
            bunnies[i][j].add(j-1)
    for k in xrange(len(times)):
        for i in xrange(len(times)):
            for j in xrange(len(times)):
                # If we have a shorter route, update the i-j times
                # and the bunnies saved alond said route
                if times[i][j] > times[i][k] + times[k][j]:
                    times[i][j] = times[i][k] + times[k][j]
                    bunnies[i][j] = bunnies[i][k].copy()
                    bunnies[i][j].update(bunnies[k][j])
    return bunnies

def solution(times, times_limit):
    route_bunnies = FloydWarshall(times)
    # If we have a negative cycle, we can rescue all the bunnies, so early-out
    for i in range(len(times)):
        if times[i][i] < 0:
            return range(len(times)-2)
    # Otherwise we need to plot the best path
    # Because we now have all the shortest routes between any two rooms, we can brute-force
    # check the 2-N length walks between the start->bunnies->bulkhead
    best_saved_bunnies = []
    from itertools import permutations
    for rlen in range(1, len(times)-1):
        for route in permutations(range(1, len(times)-1), rlen):
            route_saved_bunnies = set()
            route_time = 0
            cur_pos = 0
            # Walk the route (including to the bulkhead)
            for next_pos in list(route)+[len(times)-1]:
                route_saved_bunnies.update(route_bunnies[cur_pos][next_pos])
                route_time += times[cur_pos][next_pos]
                cur_pos = next_pos
            if route_time > times_limit:
                continue
            # Spec says we want either the most bunnies or, in the case of a tie,
            # the lowest-ID bunnies (can just compare ordered lists)
            route_saved_bunnies = sorted(list(route_saved_bunnies))
            if len(route_saved_bunnies) > len(best_saved_bunnies) or \
               route_saved_bunnies < best_saved_bunnies:
               best_saved_bunnies = list(route_saved_bunnies)
    return best_saved_bunnies

print solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)  # [1, 2]
print solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)  # [0, 1]

print solution([[0, 2, 2, 2, -10], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)  # [0, 1, 2]

print solution([[0, 1, 1, 1], [1, 0, -1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], 1)  # [0, 1]