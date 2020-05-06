import numpy as np
import cv2
import heapq

color_distance = 7.0 * 3
window_size = 5

#--------------------------------------------------------------------------------------
#---------------------------weighted adjecency-----------------------------------------
def cal_composition(img, colors):
	size = img.shape

	count_arr = np.zeros((colors.shape[0]))
	for y in range(size[0]):
		for x in range(size[1]):
			
			color_flag = False
			min_distance = color_distance+1
			min_index = -1
			for j in range(colors.shape[0]):
				distance = float(np.sum(np.abs(img[y,x,:]-colors[j,:])))
				if distance< color_distance:
					if min_distance > distance:
						min_distance = distance
						min_index = j
					color_flag = True

			if color_flag:
				count_arr[min_index] +=1

	return count_arr



def cal_weights(img, colors):
	boundary_margin = int(window_size/2)
	size = img.shape
	img_edge = cv2.Canny(img, 100, 200)

	adj = np.zeros((colors.shape[0], colors.shape[0]))

	if colors.shape[0]>=2:
		for y in range(boundary_margin,size[0]-boundary_margin):
			for x in range(boundary_margin,size[1]-boundary_margin):

				if img_edge[y,x] > 0:
					window = img[y - boundary_margin : y + boundary_margin, x - boundary_margin : x + boundary_margin]
					composition = cal_composition(window, colors)
					ind = heapq.nlargest(2,range(colors.shape[0]), composition.take)

					if composition[ind[0]] > 0 and composition[ind[1]] > 0:
						adj[ind[0],ind[1]]+=1
						adj[ind[1],ind[0]]+=1
	else:
		print('---Only one color found in the image---')
		exit()
	return adj


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
