import numpy as np
import matplotlib.pyplot as plt

# Given points for CW relations
cw_points = {
    'yolo_x': [3.14, 2.8674, 2.661, 2.387, 1.977, 1.777, 1.57],
    'yolo_y': [1.57, 1.3033, 1.101, 0.824, 0.42, 0.2057, 0],
    'robot_x': [3.14, 3.1, 3.08, 2.884, 2.76, 2.557, 2.25],
    'robot_y': [0, -0.3, -0.52, -1.2, -1.46, -1.8, -2.25]
}
# Given points for CCW relations
ccw_points = {
    'yolo_x': [0, 0.2976, 0.4536, 0.80325, 1.1258, 1.395, 1.57],
    'yolo_y': [-1.57, -1.276, -1.121, -0.7702, -0.454, -0.1705, 0],
    'robot_x': [3.14, 3.1, 3.08, 3, 2.76, 2.557, 2.25],
    'robot_y': [0, 0.3, 0.52, 0.85, 1.46, 1.8, 2.25]
}

# Fit polynomials for robot_x and robot_y for CW relations
degree = 4

coeff_x_cw = np.polyfit(cw_points['yolo_x'], cw_points['robot_x'], degree)
coeff_y_cw = np.polyfit(cw_points['yolo_y'], cw_points['robot_y'], degree)
coeff_x_ccw = np.polyfit(ccw_points['yolo_x'], ccw_points['robot_x'], degree)
coeff_y_ccw = np.polyfit(ccw_points['yolo_y'], ccw_points['robot_y'], degree)

# Define functions for the relationships
def yolo_to_robot_x(yolo_x, coeff):
    return np.polyval(coeff, yolo_x)

def yolo_to_robot_y(yolo_y, coeff):
    return np.polyval(coeff, yolo_y)

# Test the functions with the provided boundary conditions for CW
test_yolo_x_cw = np.linspace(1.57 - 0.05, 3.14 + 0.05, 100)
test_yolo_y_cw = np.linspace(0 - 0.05, 1.57 + 0.05, 100)

test_robot_x_cw = yolo_to_robot_x(test_yolo_x_cw, coeff_x_cw)
test_robot_y_cw = yolo_to_robot_y(test_yolo_y_cw, coeff_y_cw)

# Test the functions with the provided boundary conditions for CCW relations
test_yolo_x_ccw = np.linspace(0 - 0.05, 1.57 + 0.05, 100)
test_yolo_y_ccw = np.linspace(-1.57 - 0.05, 0 + 0.05, 100)

test_robot_x_ccw = yolo_to_robot_x(test_yolo_x_ccw, coeff_x_ccw)
test_robot_y_ccw = yolo_to_robot_y(test_yolo_y_ccw, coeff_y_ccw)


# Clockwise relation plot
plt.figure(figsize=(14, 8))

# Subplot for CW relations
plt.subplot(1, 2, 1)
plt.plot(cw_points['yolo_x'], cw_points['robot_x'], 'o', label='CW Points for robot_x')
plt.plot(cw_points['yolo_y'], cw_points['robot_y'], 'o', label='CW Points for robot_y')
plt.plot(test_yolo_x_cw, test_robot_x_cw, label='Interpolated curve for robot_x')
plt.plot(test_yolo_y_cw, test_robot_y_cw, label='Interpolated curve for robot_y')
plt.title('CW YOLO to Robot Coordinates Interpolation')
plt.xlabel('YOLO x or y')
plt.ylabel('Robot Coordinates')
plt.legend()
plt.grid(True)

# Subplot for CCW relations
plt.subplot(1, 2, 2)
plt.plot(ccw_points['yolo_x'], ccw_points['robot_x'], 'o', label='CCW Points for robot_x')
plt.plot(ccw_points['yolo_y'], ccw_points['robot_y'], 'o', label='CCW Points for robot_y')
plt.plot(test_yolo_x_ccw, test_robot_x_ccw, label='Extended Interpolated curve for robot_x')
plt.plot(test_yolo_y_ccw, test_robot_y_ccw, label='Extended Interpolated curve for robot_y')
plt.title('CCW YOLO to Robot Coordinates Interpolation')
plt.xlabel('YOLO x or y')
plt.ylabel('Robot Coordinates')
plt.legend()
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Show the combined plot
plt.show()

# Example: Testing with new inputs

new_yolo_x = 2.26
new_yolo_y = 0.69
if new_yolo_x >= 1.5:
    if new_yolo_y >= 0:
        coeff_x = coeff_x_cw
        coeff_y = coeff_y_cw
    else:
        coeff_x = coeff_x_ccw
        coeff_y = coeff_y_ccw
else:
    coeff_x = coeff_x_ccw
    coeff_y = coeff_y_ccw

# Using the defined functions
result_robot_x = yolo_to_robot_x(new_yolo_x, coeff_x)
result_robot_y = yolo_to_robot_y(new_yolo_y, coeff_y)

print("For YOLO x = {:f}, Robot x = {:f}".format(new_yolo_x, result_robot_x))
print("For YOLO y = {:f}, Robot y = {:f}".format(new_yolo_y, result_robot_y))
