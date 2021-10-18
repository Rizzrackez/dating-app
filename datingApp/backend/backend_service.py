import math


def calculating_distance_between_points(l1, l2, w1, w2):
    dist = math.acos(math.sin(w1) * math.sin(w2) + math.cos(w1) * math.cos(w2) * math.cos(l1 - l2))
    d = dist * 6371
    return d
