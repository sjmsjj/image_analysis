import numpy as np
import pandas as pd
from imgBase import ImageBase
from collections import defaultdict
import csv
import os
from skimage.filters import threshold_otsu

class PatternIntensity(ImageBase):
	dir_name = 'data'
	channel = None
	dist2xys = None

	def __init__(self, *args, **kwargs):
		super(PatternIntensity, self).__init__(*args, **kwargs)
		self.calculate_intensity()

	def get_things_ready(self):
		super(PatternIntensity, self).get_things_ready()
		self.cropped_image_len = self.offset*2 + 1
		self.cropped_image_cen = self.offset + 1
		self.get_dist2xys_mapping()
		self.calculate_intensity()

	def get_dist2xys_mapping(self):
		if self.dist2xys is None:
			self.dist2xys = defaultdict(list)
			for row in xrange(self.cropped_image_len):
				for col in xrange(self.cropped_image_len):
					distance = np.sqrt(np.power(row-self.cropped_image_cen, 2) + np.power(col-self.cropped_image_cen, 2))/self.MICRO_TO_PIXEL
					self.dist2xys[distance].append([row, col])
		self.dist_list = sorted(self.dist2xys.keys())
		return self.dist2xys

	def calculate_intensity(self):
		for image_path, image_name in self.images:
			print "Processing image: " + image_name
			group, channel = image_name.split('.')[0].split('_')
			gray_img = self.get_gray_images(image_path)
			global_thresh = threshold_otsu(gray_img)
			intensity_values = [0]*len(self.dist_list)
			for index, dist in enumerate(self.dist_list):
				ncoords = 0
				for coord in self.dist2xys[dist]:
					intensity = gray_img[coord[0]][coord[1]]
					if intensity > global_thresh:
						intensity_values[index] += intensity
						ncoords += 1
				if ncoords == 0:
					if index > 0:
						intensity_values[index] = intensity_values[index-1]
				else:
					intensity_values[index] /= ncoords
			self.save_data(image_name, intensity_values, channel)

	def save_data(self, image_name, intensity_values, channel):
		file_name = image_name.split('.')[0] + '.csv'
		with open(os.path.join(self.output_data_dir, file_name), 'w') as f:
			writer = csv.writer(f, delimiter=',')
			writer.writerow(('distance', channel))
			for dist, intensity in zip(self.dist_list, intensity_values):
				writer.writerow((dist, intensity))

if __name__ == '__main__':
	t = PatternIntensity()


