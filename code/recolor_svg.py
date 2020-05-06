import numpy as np
from scipy.optimize import linear_sum_assignment
import sys
import color_graph
import CompositionVec
import recolor_util
from svg_to_png import svg2png

files = sys.argv
inputFilename = files[1]
referenceFilename = files[2]
namedColorsFilename = './rgb.txt'
epcilon = 0.001

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
def hungarian_matching(cost_matrix):
	row_ind, col_ind = linear_sum_assignment(cost_matrix)
	row_ind = list(row_ind)
	col_ind = list(col_ind)
	matchingList = []
	for i in range(len(row_ind)):
		temp = col_ind[row_ind.index(i)]
		matchingList.append(temp)

	return matchingList

#----------------------------------------------------------------------------------------
#---------------New neighbourhood cost based eigendecomposition color matching-----------

#m1[i,j]= distance between ith color of matrix1 and jth color of matrix2
def compositionCost(composition1, composition2):
	size = composition1.shape[0]
	m1 = np.zeros((size,size)).astype('float')

	for i in range(size):
		for j in  range(size):
			m1[i,j] = np.abs(composition1[i] - composition2[j])
	m1 = m1/(m1.max()+epcilon)
	return m1

def EigenDecomposition(matrix1, matrix2):
	w1,U1 = np.linalg.eig(matrix1)
	w2,U2 = np.linalg.eig(matrix2)
	U1_bar = np.abs(U1)
	U2_bar = np.abs(U2)
	matrix = np.matmul(U2_bar,np.transpose(U1_bar))
	return matrix/np.max(matrix)


def EigenDecomposition_Color_matching(inputAjdacency, referenceAjdacency, inputComposition, referenceComposition):

	#normalising adjacency weights
	temp = np.sum(inputAjdacency)
	if temp>0:
		inputAjdacency = (inputAjdacency*2)/temp

	temp = np.sum(referenceAjdacency)
	if temp>0:
		referenceAjdacency = (referenceAjdacency*2)/temp
	

	neigh_cost_matrix = EigenDecomposition(inputAjdacency, referenceAjdacency)
	neigh_cost_matrix = np.max(neigh_cost_matrix) - neigh_cost_matrix
	
	composition_cost_matrix = compositionCost(inputComposition, referenceComposition)

	cost_matrix = neigh_cost_matrix + composition_cost_matrix #neighbourhood + composition cost

	matchingList = hungarian_matching(cost_matrix)

	matchingCost = np.sum(cost_matrix[np.arange(inputAjdacency.shape[0]), matchingList])
	return matchingList, matchingCost

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
def calCompositionAndAdjacency(filename):
	palette = recolor_util.get_palette_from_svg(namedColorsFilename, filename)
	colors = np.array(list(palette.values()))
	img = svg2png(filename)

	colors, composition = CompositionVec.compute_composition(img, colors)

	ajdacency = color_graph.cal_weights(img, colors)
	return colors, composition, ajdacency

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

if __name__=='__main__':
	
	inputColors, inputComposition, inputAjdacency = calCompositionAndAdjacency(inputFilename)
	# print(inputColors)
	# print(inputComposition)
	# exit()
	referenceColors, referenceComposition, referenceAjdacency = calCompositionAndAdjacency(referenceFilename)

	print('----Compositions and Adjacency matrices calculated ----')
	print('number of colors in input and reference image', inputColors.shape[0], referenceColors.shape[0])
	if inputColors.shape[0]>referenceColors.shape[0]:
		print('---reference color palette has lesser colors than input color palette---')
		inputColors = inputColors[:referenceColors.shape[0], :]
		inputComposition = inputComposition[:referenceColors.shape[0]]
		inputAjdacency = inputAjdacency[:referenceColors.shape[0], :referenceColors.shape[0]]
	else:
		referenceColors = referenceColors[:inputColors.shape[0], :]
		referenceComposition = referenceComposition[:inputColors.shape[0]]
		referenceAjdacency = referenceAjdacency[:inputColors.shape[0], :inputColors.shape[0]]

	matchingList, matchingCost = EigenDecomposition_Color_matching(inputAjdacency, referenceAjdacency, inputComposition, referenceComposition)
	print('***Color matching is done***')

	recoloredSVG = recolor_util.recolor(namedColorsFilename, inputFilename, inputColors, referenceColors, matchingList)
	# Write the file out again
	with open(inputFilename.rstrip('.svg')+'Recolored.svg', 'w') as file:
		file.write(recoloredSVG)
	print('---output coloring has been generated---')

#---------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
