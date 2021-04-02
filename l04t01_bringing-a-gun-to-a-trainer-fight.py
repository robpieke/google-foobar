'''
Bringing a Gun to a Trainer Fight
=================================

Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully).

Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).

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
Solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
Solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9

-- Python cases --
Input:
solution.solution([3,2], [1,1], [2,1], 4)
Output:
    7

Input:
solution.solution([300,275], [150,150], [185,100], 500)
Output:
    9
'''


def solution(dimensions, your_position, trainer_position, distance):

    def gcd(x, y):
        x, y = min(x, y), max(x, y)
        while x != 0:
            x, y = y%x, x
        return y

    def calculate_bounce_distances(start, end, dim, max_dist):
        distances = [end-start]
        # For a given distance we know the limit on the number of bounces
        for i in range(1, max_dist/dim + 2):
            # These were painfully worked out by hand (lots of sketching of bouncing rays)
            if i % 2 == 0:
                distances.append(-(i*dim - (end - start)))
                distances.append(  i*dim + (end - start))
            else:
                distances.append(-((i-1)*dim + (end + start)))
                distances.append(  (i+1)*dim - (end + start))
        return distances

    def generate_bearing_routes(distances_x, distances_y, max_dist, filter_routes = None):
        routes = {}
        max_dist_sq = max_dist**2;
        for dx, dy in [(dx, dy) for dx in distances_x for dy in distances_y]:
            d_sq = dx**2 + dy**2
            if d_sq == 0 or d_sq > max_dist_sq:
                continue
            gcd_abs = abs(gcd(dx, dy))
            dx /= gcd_abs
            dy /= gcd_abs
            key = (dx, dy)
            if filter_routes and key in filter_routes and filter_routes[key] < d_sq:
                continue
            if key in routes and routes[key] < d_sq:
                continue
            routes[(dx, dy)] = d_sq
        return routes

    dim = dimensions
    pos1 = your_position
    pos2 = trainer_position
    max_dist = distance

    # Find the N-bounce distances for self hits
    distances_s = [calculate_bounce_distances(pos1[0], pos1[0], dim[0], max_dist),
                   calculate_bounce_distances(pos1[1], pos1[1], dim[1], max_dist)]
    routes_s = generate_bearing_routes(distances_s[0], distances_s[1], max_dist)

    # Same for trainer hits, filtering against self hits
    distances_t = [calculate_bounce_distances(pos1[0], pos2[0], dim[0], max_dist),
                   calculate_bounce_distances(pos1[1], pos2[1], dim[1], max_dist)]
    routes_t = generate_bearing_routes(distances_t[0], distances_t[1], max_dist, routes_s)

    return len(routes_t)


print solution([3,2], [1,1], [2,1], 4)  # 7
print solution([300,275], [150,150], [185,100], 500)  # 9

print solution([3,2], [1,1], [2,1], 1)  # 1
