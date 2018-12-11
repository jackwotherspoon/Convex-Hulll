#Author: Jack Wotherspoon
#Created: Nov. 2nd, 2018
from matplotlib import pyplot as plt  # for plotting
from random import randint  # for sorting and creating data pts
from math import atan2, sqrt  # for computing polar angle

def create_points(ct, min=-200, max=200):
    return [[randint(min, max), randint(min, max)] \
            for _ in range(ct)]

def scatter_plot(coords, convex_hull=None):
    xs, ys = zip(*coords)
    plt.scatter(xs, ys)

    if convex_hull != None:
        for i in range(1, len(convex_hull) + 1):
            if i == len(convex_hull): i = 0
            c0 = convex_hull[i - 1]
            c1 = convex_hull[i]
            plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')
    plt.show()

# 'graham_scan' function.
def polar_angle(p0, p1=None):
    if p1 == None: p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return atan2(y_span, x_span)

# 'graham_scan' function.
def distance(p0, p1=None):
    if p1 == None: p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return y_span ** 2 + x_span ** 2

def det(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) \
           - (p2[1] - p1[1]) * (p3[0] - p1[0])

def quicksort(a):
    if len(a) <= 1: return a
    smaller, equal, larger = [], [], []
    piv_ang = polar_angle(a[randint(0, len(a) - 1)])  # select random pivot
    for pt in a:
        pt_ang = polar_angle(pt)  # calculate current point angle
        if pt_ang < piv_ang:
            smaller.append(pt)
        elif pt_ang == piv_ang:
            equal.append(pt)
        else:
            larger.append(pt)
    return quicksort(smaller) \
           + sorted(equal, key=distance) \
           + quicksort(larger)

def graham_scan(points, show_progress=False):
    global anchor

    min_idx = None
    for i, (x, y) in enumerate(points):
        if min_idx == None or y < points[min_idx][1]:
            min_idx = i
        if y == points[min_idx][1] and x < points[min_idx][0]:
            min_idx = i
    anchor = points[min_idx]


    sorted_pts = quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)]

    hull = [anchor, sorted_pts[0]]
    for s in sorted_pts[1:]:
        while det(hull[-2], hull[-1], s) <= 0:
            del hull[-1]  # backtrack

        hull.append(s)
        if show_progress: scatter_plot(points, hull)
    return hull

def benchmark(sizes=[10, 100, 1000, 10000, 100000]):
    for s in sizes:
        tot = 0.0
        for _ in range(3):
            pts = create_points(s, 0, max(sizes) * 10)
            t0 = time()
            hull = graham_scan(pts, False)
            tot += (time() - t0)
        print("size %d time: %0.5f" % (s, tot / 3.0))


def bounding_circle(middle_points, hull_points):

    radius = []
    for point in hull_points:
        radi = sqrt(distance(middle_points, point))
        radius.append(radi)
    R = max(radius)
    return middle_points, R


def avg_middles(list_):
    x, y = zip(*list_)
    middle_points = []
    x_avg = (sum(x)/len(x))
    y_avg = (sum(y)/len(y))
    middle_points.append(x_avg)
    middle_points.append(y_avg)
    return middle_points


def intersection_check(points_1, points_2, R1, R2):  # circle = (x, y, R)
    x1, y1 = points_1
    x2, y2 = points_2
    if (R1 - R2) ** 2 <= ((x1-x2) ** 2 + (y1-y2) ** 2) and ((x1-x2) ** 2 + (y1-y2)) <= (R1+R2) ** 2:
        print("They Do Intersect")  # they do intersect
    else:
        print("They Do Not Intersect")  # they don't intersect

def circle_plot(coords_1, convex_hull_1, mid_points_1, r1, mid_points_2, r2, coords_2, convex_hull_2):
    xs1, ys1 = zip(*coords_1)
    xs2, ys2 = zip(*coords_2)
    plt.scatter(xs1, ys1)
    plt.scatter(xs2, ys2, color='orange')
    x1, y1 = mid_points_1
    x2, y2 = mid_points_2
    circ1 = plt.Circle((x1, y1), r1, color='blue', fill=False)
    circ2 = plt.Circle((x2, y2), r2, color='red', fill=False)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.add_patch(circ1)
    ax.add_patch(circ2)
    if convex_hull_1 != None:
        for i in range(1, len(convex_hull_1) + 1):
            if i == len(convex_hull_1): i = 0
            c0 = convex_hull_1[i - 1]
            c1 = convex_hull_1[i]
            plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'b')
    if convex_hull_2 != None:
        for i in range(1, len(convex_hull_2) + 1):
            if i == len(convex_hull_2): i = 0
            c0 = convex_hull_2[i - 1]
            c1 = convex_hull_2[i]
            plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')
    plt.show()


pts = create_points(100)
# print("Points:", pts)
hull = graham_scan(pts, False)
# print(len(hull))
scatter_plot(pts, hull)
# # fig = plt.figure()
# # middle_pts, bc = bounding_circle(avg_middles(pts), hull)
# # circle = plt.Circle(middle_pts, int(bc))
# # ax = fig.add_subplot(1, 1, 1)
# # ax.add_artist(circle)
# # plt.plot(100,100)
# #
# # plt.show()
