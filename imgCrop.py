import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import misc 
from imgBase import ImageBase

class ImageCrop(ImageBase):
	dir_name = 'cropped_images'
	pre_image = None
	curr_image = None

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
			cropped_image = self.get_cropped_image(raw_image)
			self.save_image(cropped_image, image_name)
			pre_group = curr_group

	def save_image(self, image, image_name):
		misc.imsave(self.output_data_dir +'/' + image_name, image)

if __name__ == '__main__':
	t = ImageCrop()

