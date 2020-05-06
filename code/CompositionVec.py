import numpy as np
import heapq

#-----------------------------------------------------------------------------------------
#------------------RGB image and when palette is known--------------------------------

def compute_composition(img, colors_arr):
	num_colors = colors_arr.shape[0]

	size = img.shape
	dictionary_coordinate = {i:[] for i in range(num_colors)} #will contain list of coordinates for each color

	flag_count = 0
	composition = [0 for i in range(num_colors)]

	for y in range(size[0]):
		for x in range(size[1]):
			
			distance = np.zeros(num_colors)
			for j in range(num_colors):
				distance[j] = np.linalg.norm(np.abs(img[y,x,:] - colors_arr[j,:]))

			min_index = np.argmin(distance)
			composition[min_index] +=1
			dictionary_coordinate[min_index].append(np.array([x, y]))

	composition = np.array(composition).astype('float')

	ordered_ind = heapq.nlargest(num_colors,range(num_colors), composition.take)

	for i in range(num_colors): #normalising composition with size of image.
		composition[i] = composition[i]/(size[0]*size[1])

	ordered_composition = []
	ordered_colors = []
	ordered_dictionary_coordinate = {}
	key_itr = 0
	for i in ordered_ind:
		if composition[i]>0.02: #Colors with atleast 2% composition are considered
			ordered_composition.append(composition[i])
			ordered_colors.append(colors_arr[i,:])
			ordered_dictionary_coordinate[key_itr]= dictionary_coordinate[i]
			key_itr+=1

	colors_arr = np.array(ordered_colors).astype('float')
	composition = np.array(ordered_composition).astype('float')

	return(colors_arr, composition)
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------

