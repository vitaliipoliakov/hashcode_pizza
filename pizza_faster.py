import numpy as np
import math
import sys
import matplotlib.pyplot as plt


last_pos = 0

# @profile
def read_input(file):
	csv = open(file, 'r').readlines()
	[r, c, l, h] = [int(val) for val in csv[0].split(' ')]
	pizza = np.array([list(map(lambda char : 1 if char=='T' else 0, row.strip())) for row in csv[1:]])
	return (r, c, l, h, pizza)

# @profile
def write_output(filename, pizza_slices):
    """Writes an output file with the required format."""
    with open(filename, 'w') as f:
        f.write(str(len(pizza_slices))+"\n")
        for slice in pizza_slices:
            r, c, dr, dc = slice
            f.write(str(r)+" "+str(c)+" "+str(dr)+" "+str(dc)+"\n")

# @profile
def gen_map(pizza):
	# print(len(pizza))
	# 0 means free, 1 will mean that cell belongs to a slice
	return np.array([ [0 for i in range(len(pizza[0]))] for j in range(len(pizza)) ])

# @profile
def confirm_slice(l, row, column, shape, pizza, slice_map):
	# check if it fits
	check = slice_map[row:row+shape[0], column:column+shape[1]]
	if np.sum(check) > 0:
		return 0
	# continue to confirm the constraints
	new_slice = pizza[row:row+shape[0], column:column+shape[1]]
	t = 0
	m = 0
	# print(new_slice)
	for row in new_slice:
		for cell in row:
			if cell == 1:
				t = t + 1
			else:
				m = m + 1
	if t >= l and m >= l:
		return 1
	else:
		return 0
	pass

# @profile
def gen_cell_dict(r, c):
	return {i : 'a' for i in range(r*c)}

# @profile
def gen_cell_list(r, c):
	# 0 means available
	return [0 for i in range(r*c)]

# @profile
def gen_shapes(r, c, l, h):
	shapes = []
	for hh in range(l*2, h+1):
		factors = []
		for i in range(1, hh+1):
			if hh % i == 0:
				factors.append(i)
		for i in factors:
			if max(i, hh/i) <= min(r, c):
				shapes.append([i, int(hh/i)])
	return shapes

# @profile
def get_cell(array, last):
	pos = 0
	i = -1
	for row in array:
		i = i + 1
		if i < last:
			pos = pos+len(row)
			continue
		for cell in row:
			if cell == 0:
				# print(row, pos)
				return [pos, i-1]
			pos = pos + 1
	return [-1, -1] # if no cells left

# @profile
def cut_slice(row, column, shape, slice_map):#, cell_dict):
	# 1 is taken by a slice
	slice_map[row:row+shape[0], column:column+shape[1]] = 1
	slice_coords = [row, column, row+shape[0]-1, column+shape[1]-1]
	return [slice_map, slice_coords]#[slice_map, cell_dict]

# @profile
def behaviour(r, c, l, h, pizza, slice_map, cell_dict):
	shapes = gen_shapes(r, c, l, h)
	# print('shapes: ',shapes)

	cell = 0
	total_slices = 0
	slices = []
	area_sliced = 0
	last = 0
	while cell >= 0:
		# print('current cell:',cell)
		if cell % 100 == 0:
			print('current cell:',cell)

		# cell = next(iter(cell_dict)) # for dict
		# cell = get_cell(cell_dict) # for list
		[cell, last] = get_cell(slice_map, last)

		[row, column] = [math.trunc(cell/c), cell%c]

		# just oterate over the shapes and get the first that fits
		# shapes are ordered from smalles to biggest
		shape = 0
		for s in shapes:
			check = confirm_slice(l, row, column, s, pizza, slice_map)
			if check == 1:
				break
			shape = shape + 1

		# if the starting cell cannot be used for a shape, 
		# remove it from dict
		if shape >= len(shapes):
			[slice_map, out] = cut_slice(row, column, [1, 1], slice_map)
		else:
			# otherwise cut the actual slice
			area_sliced = area_sliced + (shapes[shape][0] * shapes[shape][1])
			[slice_map, out] = cut_slice(row, column, shapes[shape], slice_map)
			total_slices = total_slices + 1
			slices.append(out)
	print('Total slices:',total_slices)
	print('Total area:',area_sliced)
	# print('Coordinates of all slices:')
	# print(slices)

	return slices


def main():
	[r, c, l, h, pizza] = read_input(sys.argv[1])
	# print(pizza)

	fig, ax = plt.subplots()
	ax.imshow(pizza)

	slice_map = np.array(gen_map(pizza.tolist())) # fix this abomination
	# cell_dict = gen_cell_dict(r, c)
	cell_dict = gen_cell_list(r, c)
	print(slice_map)
	slices = behaviour(r, c, l, h, pizza, slice_map, cell_dict)

	write_output(sys.argv[1]+".out", slices)


if __name__ == '__main__':
	main()