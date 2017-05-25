# image_analysis
A simple image analysis program which extracts the largest pattern in a image and calculate the average color intensity from the center to the border.

imgBase.py
	Base class.

imgColor.py
	Color each image under a dir.

imgCrop.py	
	Crop each image under a dir.

imgData.py
	Generate the radial intensity profile of cropped images under a dir. 
	It writes the intensity profile into a .csv file for each image.

imgObserve.py
	Observe individual images under microscope. Operations include plotting raw_img, binary_img, closed_img, centroid, histogram, etc. 
