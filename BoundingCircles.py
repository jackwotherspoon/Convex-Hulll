#Author:Jack Wotherspoon
#Created: Nov. 2nd, 2018
import grahamScan as gs

pts_1 = gs.create_points(10, -100, 100)
pts_2 = gs.create_points(10, -100, 100)
print("points 1: ", pts_1)
print("points 2: ", pts_2)
hull_1 = gs.graham_scan(pts_1, False)
hull_2 = gs.graham_scan(pts_2, False)
print("hull 1: ", hull_1)
print("hull 2: ", hull_2)

middle_points_1 = gs.avg_middles(pts_1)
middle_points_2 = gs.avg_middles(pts_2)

middle_points_1, R1 = gs.bounding_circle(gs.avg_middles(pts_1), hull_1)
middle_points_2, R2 = gs.bounding_circle(gs.avg_middles(pts_2), hull_2)


gs.circle_plot(pts_1, hull_1, middle_points_1, R1, middle_points_2, R2, pts_2, hull_2)

gs.intersection_check(middle_points_1, middle_points_2, R1, R2)






