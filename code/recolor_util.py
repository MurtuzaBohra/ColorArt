from colormap import rgb2hex
import re
import numpy as np

colorDistance = float(7*3)
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def find_word(word_list, line):
	words_present = []
	for word in word_list:
		if word in line:
			words_present.append(word)
	return words_present


def hex2rgb(hexColor):
	if hexColor[0] == '#': hexColor = hexColor[1:]
	elif hexColor[0:2].lower() == '0x': hexColor = hexColor[2:]
	if len(hexColor) < 6: hexColor = hexColor[0]+'0'+hexColor[1]+'0'+hexColor[2]+'0'
	return int(hexColor[0:2], 16), int(hexColor[2:4], 16), int(hexColor[4:6], 16)

def read_named_color(filename):
	word_list = []
	word_rgb_dict = {}
	for i, line in enumerate(open(filename)):
		if i!=0:
			temp = line.split()
			j=4
			strg = temp[3]
			while( j < len(temp)):
				strg = strg+' '+temp[j]
				j+=1

			word_list.append(strg)
			word_rgb_dict[strg] = (float(temp[0]), float(temp[1]), float(temp[2]))
	return word_rgb_dict, word_list


def get_palette_from_svg(namedColorsFilename, svgFilename):
	palette = []
	pattern = re.compile("#[a-fA-F0-9\d]{6}|#[a-fA-F0-9]{3}")

	for i, line in enumerate(open(svgFilename)):
		for match in re.finditer(pattern, line):
			hexcolor = match.group(0).lower()
			palette.append(hexcolor)

	palette = list(set(palette))
	palette_dict ={}
	for ele in palette:
		r,g,b = hex2rgb(ele) 
		palette_dict[ele] = (float(r), float(g), float(b))

	#by default, background is set to white color while converting svg to png.
	palette_dict['#ffffff'] = (255.0, 255.0, 255.0)

	word_rgb_dict, word_list = read_named_color(namedColorsFilename)
	with open(svgFilename, 'r') as f:
		result = []
		for line in f.readlines():
			result = result + find_word(word_list, line) 
		result = list(set(result))

	for ele in result:
		palette_dict[ele] = word_rgb_dict[ele]

	return palette_dict

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def createRecoloredSvg(svgFilename, replaceColorDict):
	with open(svgFilename, 'r') as file :
		filedata = file.read()

	# Replace the target string
	for key, value in replaceColorDict.items():
		filedata = filedata.replace(key.upper(), value)
		filedata = filedata.replace(key, value)
	return filedata



def recolor(namedColorsFilename, svgFilename, inputColors, referenceColors, matchingList):

	paletteDict = get_palette_from_svg(namedColorsFilename, svgFilename)

	numColors = inputColors.shape[0]

	replaceColorDict = {}#will store the mapping of colors from input image to reference image

	for key, value in paletteDict.items():
		color_flag = False
		min_distance = colorDistance+1
		min_index = -1
		for i in range(numColors):
			distance = np.sum(np.abs(np.array(value)-inputColors[i,:]))

			if distance < colorDistance:
				# print('****')
				if min_distance > distance:
					min_distance = distance
					min_index = i
				color_flag = True

		if color_flag:
			replaceWith = referenceColors[matchingList[min_index],:]
			hexcode = rgb2hex(int(replaceWith[0]), int(replaceWith[1]), int(replaceWith[2]))
			replaceColorDict[key] = hexcode
				
	recoloredSVG = createRecoloredSvg(svgFilename, replaceColorDict)
	return recoloredSVG

#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
