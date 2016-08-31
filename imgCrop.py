import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import misc 
from imgBase import ImageBase
from collections import defaultdict

class ImageCrop(ImageBase):
	dir_name = 'cropped_images'
	pattern_size = defaultdict(list)

	def __init__(self, *args, **kwargs):
		super(ImageCrop, self).__init__(*args, **kwargs)
		self.crop_images()

	def crop_images(self):
		pre_group = None
		curr_group = None
		for image_path, image_name in self.images:
			print image_name
			curr_group = image_name.split('.')[0].split('_')[0]
			raw_image, _, closed_image = self.get_images(image_path)
			if not pre_group or pre_group != curr_group:
				self.get_pattern_centroid(closed_image)
				self.get_pattern_border(closed_image)
				self.get_pattern_size(image_name)
			cropped_image = self.get_cropped_image(raw_image)
			self.save_image(cropped_image, image_name)
			pre_group = curr_group
	    self.save_pattern_size()

	def get_pattern_size(self, image_name):
		substrate = image_name.split('-')[-2]
		size = (self.circle.major_axis_length+self.circle.minor_axis_length)/2
		self.pattern_size[substrate].append(size)

	def save_pattern_size(self):
		df = pd.DataFrame()
		for key, val in self.pattern_size.items():
			df[key] = val
		df.to_csv(os.path.join(self.output_data_dir, 'pattern_size'), index=False)

	def save_image(self, image, image_name):
		misc.imsave(self.output_data_dir +'/' + image_name, image)

if __name__ == '__main__':
	t = ImageCrop()

