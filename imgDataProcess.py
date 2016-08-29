import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import os
from imgBase import ImageBase


class ImageDataProcess(ImageBase):
	data_dir = None
	dir_name = 'reduced_data'

	def __init__(self, *args, **kwargs):
		super(ImageDataProcess, self).__init__(*args, **kwargs)
		self.reduce_data()

	def get_things_ready(self):
		self.create_output_data_dir()
		if not self.data_dir:
			self.data_dir = self.image_dir

	def reduce_data(self):
		for file_path, file_name in self.get_image_data_files():
			print file_name
			data = self.read_image_data(file_path)
			reduced_data = pd.DataFrame(columns=data.columns)
			lower = higher = 0
			for i in xrange(1, self.diameter/2+1):
				higher = np.power(self.MICRO_TO_PIXEL*i, 2)
				ring_data = data.loc[lower:higher-1]
				reduced_data.loc[i] = ring_data.mean()
				lower = higher
			self.save_data(reduced_data, file_name)

	def save_data(self, data, file_name):
		data.to_csv(os.path.join(self.output_data_dir, file_name))

	def get_image_data_files(self):
		for root, directories, files in os.walk(self.data_dir):
			if root == self.output_data_dir:
				continue
			for file_name in files:
				if file_name.endswith('.csv'):
					file_path = os.path.join(root, file_name)
					yield file_path, file_name

	def read_image_data(self, file_path):
		return pd.read_csv(file_path, index_col=0)

if __name__ == '__main__':
	t = ImageDataProcess()
	


