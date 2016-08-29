import numpy as np
import pandas as pd
from imgBase import ImageBase
from collections import defaultdict
import csv
import os
from skimage.filters import threshold_otsu

class PatternIntensity(ImageBase):
	dir_name = 'data'
	df_mold = None
	curr_df = None
	pre_image = None
	curr_image = None
	channel = None
	dist2xys = None

	def __init__(self, *args, **kwargs):
		super(PatternIntensity, self).__init__(*args, **kwargs)
		# self.calculate_intensity()

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



	# def get_image_intensity(self, image_path):
	# 	image = self.get_gray_images(image_path)
	# 	for index in self.curr_df.index:
	# 		for row, col in self.dist2xys[index]:
	# 			self.curr_df.loc[index][self.channel] += image[row][col]

	# def save_data(self):
	# 	file_name = self.pre_image + '.csv'
	# 	self.curr_df = self.curr_df.div(self.curr_df['count'], axis=0)
	# 	self.curr_df.drop('count', axis=1, inplace=True)
	# 	self.curr_df.to_csv(os.path.join(self.output_data_dir, file_name))

	# def get_new_df(self):
	# 	self.curr_df = self.df_mold.copy(deep=True)
	# 	self.curr_df[self.channel] = 0
	# 	return self.curr_df

	# def create_df_mold(self):
	# 	if self.df_mold is None:
	# 		map_entry = sorted(self.dist2xys.items(), key=lambda item: item[0])
	# 		index = [entry[0] for entry in map_entry]
	# 		counts = [len(entry[1]) for entry in map_entry]
	# 		self.df_mold = pd.DataFrame(counts, index=index, columns=['counts'])
	# 	return self.df_mold

	# def create_df_mold(self):
	# 	if not self.df_mold:
	# 		pixels = int(self.diameter * self.MICRO_TO_PIXEL)
	# 		center = pixels/2
	# 		distances = {}
	# 		for row in xrange(pixels):
	# 			for col in xrange(pixels):
	# 				index = np.power(row-center, 2) + np.power(col-center, 2)
	# 				distances[index] = distances.get(index, 0) + 1
	# 		items = sorted(distances.items(), key=lambda item:item[0])
	# 		index = [item[0] for item in items]
	# 		counts = [item[1] for item in items]
	# 		self.df_mold = pd.DataFrame(counts, index=index, columns=['count'])
	# 	return self.df_mold

if __name__ == '__main__':
	t = PatternIntensity()


