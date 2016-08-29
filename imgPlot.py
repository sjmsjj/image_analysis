import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import os
from imgBase import ImageBase


class ImagePlot(ImageBase):
	data_dir = None
	image_data = None

	def __init__(self, *args, **kwargs):
		super(ImagePlot, self).__init__(*args, **kwargs)
		print "done"

	def get_things_ready(self):
		if not self.data_dir:
			self.data_dir = self.image_dir
		if self.image_data is None:
			self.average_image_data()
			self.normalize_image_data()

	def plot(self, *args):
		data = self.get_plot_data(*args)
		data.plot()
		plt.ylim(ymax=1.2)
		plt.show()

	def get_plot_data(self, *args):
		col_filter = self.make_fileter(*args)
		selected_columns = filter(col_filter, self.image_data.columns)
		return self.image_data[selected_columns]
	
	def make_fileter(self, *args):
		def col_filter(col):
			for key in args:
				if key not in col:
					return False
			return True 
		return col_filter

	def average_image_data(self):
		pre_group = None
		curr_group = None
		group_data = None
		nimages = 0

		for file_path, file_name in self.get_image_data_files():
			data = self.read_image_data(file_path)
			curr_group = file_name.split('.')[0][:-5]
			self.rename_columns(data, curr_group)
			if group_data is None:
				group_data = data
				nimages = 1
			elif pre_group == curr_group:
				group_data += data
				nimages += 1
			elif pre_group != curr_group:
				group_data /= nimages
				if self.image_data is None:
					self.image_data = group_data
				else:
					self.image_data = pd.concat([self.image_data, group_data], axis=1)
				group_data = data
				nimages = 1
			pre_group = curr_group
		return self.image_data

	def normalize_image_data(self):
		self.image_data = (self.image_data - self.image_data.min())/(self.image_data.max()-self.image_data.min())

	def get_image_data_files(self):
		for file_name in os.listdir(self.data_dir):
			if file_name.endswith('.csv'):
				file_path = os.path.join(self.data_dir, file_name)
				yield file_path, file_name

	def read_image_data(self, file_path):
		return pd.read_csv(file_path, index_col=0)

	def rename_columns(self, data, curr_group):
		columns = data.columns
		new_columns = [curr_group + '.' + col for col in columns]
		data.columns = new_columns

if __name__ == '__main__':
	t = ImagePlot()
	


