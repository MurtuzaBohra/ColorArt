import os
import cv2

def svg2png(svgFilename):
	pngFilename = svgFilename.rstrip('.svg')+'.png'

	try:
		cmd = "inkscape -z -e "+pngFilename+" -w 256 -b \'#ffffff\' "+svgFilename+""
		os.system(cmd)
	except:
		print('***could not convert svg to png***')
		exit()
	img = cv2.imread(pngFilename)

	cmd = "rm "+pngFilename+""
	os.system(cmd)
	return(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#-------------------------------------------------------------
#-------------------------------------------------------------