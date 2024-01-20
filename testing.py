# Read values from the text file
file_path = "runs\detect\exp25\labels\color_image1.txt"

with open(file_path, 'r') as file:
    values = file.readline().split()

# Initialize the dictionary
bb_dict = {}

# Assign values to dictionary keys
bb_dict['upper_right'] = {'x': int(float(values[1])), 'y': int(float(values[2])) }
bb_dict['bottom_right'] = {'x': int(float(values[3])), 'y': int(float(values[4])) }
bb_dict['bottom_left'] = { 'x': int(float(values[5])), 'y': int(float(values[6])) }
bb_dict['upper_left'] = { 'x': int(float(values[7])), 'y': int(float(values[8])) }

print(bb_dict)