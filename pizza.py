import numpy as np
import math
import sys
import matplotlib.pyplot as plt


last_pos = 0


def read_input(file):
	csv = open(file, 'r').readlines()
	[r, c, l, h] = [int(val) for val in csv[0].split(' ')]
	pizza = np.array([list(map(lambda char : 1 if char=='T' else 0, row.strip())) for row in csv[1:]])
	return (r, c, l, h, pizza)


def gen_map(pizza):
	# print(len(pizza))
	# 0 means free, 1 will mean that cell belongs to a slice
	return np.array([ [0 for i in range(len(pizza[0]))] for j in range(len(pizza)) ])


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


def gen_cell_dict(r, c):
	return {i : 'a' for i in range(r*c)}


def gen_cell_list(r, c):
	# 0 means available
	return [0 for i in range(r*c)]


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


# only for a list for now
def get_cell(array):
	pos = 0
	for row in array:
		for cell in row:
			if cell == 0:
				last_pos = pos
				return pos
			pos = pos + 1
	return -1 # if no cells left


def cut_slice(row, column, shape, slice_map):#, cell_dict):
	# 1 is taken by a slice
	slice_map[row:row+shape[0], column:column+shape[1]] = 1
	slice_coords = [row, column, row+shape[0]-1, column+shape[1]-1]
	return [slice_map, slice_coords]#[slice_map, cell_dict]


def behavour(r, c, l, h, pizza, slice_map, cell_dict):
	# slice_map = gen_map(pizza.tolist())
	shapes = gen_shapes(r, c, l, h)
	# print('shapes: ',shapes)

	cell = 0
	total_slices = 0
	slices = []
	area_sliced = 0
	while cell >= 0:
		# print('current cell:',cell)
		if cell % 100 == 0:
			print('current cell:',cell)

		# cell = next(iter(cell_dict)) # for dict
		# cell = get_cell(cell_dict) # for list
		cell = get_cell(slice_map)

		[row, column] = [math.trunc(cell/c), cell%c]

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
	print('Coordinates of all slices:')
	print(slices)
	pass


def main():
	[r, c, l, h, pizza] = read_input(sys.argv[1])
	# print(pizza)

	fig, ax = plt.subplots()
	ax.imshow(pizza)

	slice_map = np.array(gen_map(pizza.tolist())) # fix this abomination
	# cell_dict = gen_cell_dict(r, c)
	cell_dict = gen_cell_list(r, c)
	print(slice_map)
	behavour(r, c, l, h, pizza, slice_map, cell_dict)


if __name__ == '__main__':
	main()





# print(h)
# print(pizza[1][3])



# 'a_example.in'
















# import pandas as pd

# csv = pd.read_csv('a_example.in', header=0)
# print(csv.values)
# a = csv.values
# print(a[0][0][1])

# import csv

# f = open('a_example.in', 'r')
# with f:
# 	reader = csv.reader(f, delimiter=' ')

# 	header = reader.__next__()
# 	# print(header[3])

# 	pizza = []
# 	for row in reader:
# 		tmp = []
# 		for cell in row:
# 			print(cell)
# 			tmp.append(cell)
# 		pizza.append(tmp)

	# print(pizza)