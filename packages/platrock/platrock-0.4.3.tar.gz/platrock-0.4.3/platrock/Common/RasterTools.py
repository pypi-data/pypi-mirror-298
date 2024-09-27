"""
"""

import numpy as np
import copy
from osgeo import gdal


def from_terrain(terrain,cell_length,xllcorner=0,yllcorner=0):
	"""
	Create a new raster from the terrain only. /!\ if the terrain was generated from an asc, please use "from_asc" then "from_raster" to avoid shifting of the origin.
	"""
	r=Raster()
	xmin=terrain.points_as_array[:,0].min()
	xmax=terrain.points_as_array[:,0].max()
	ymin=terrain.points_as_array[:,1].min()
	ymax=terrain.points_as_array[:,1].max()
	r.cell_length=float(cell_length)
	r.X=np.arange(xmin,xmax+cell_length,cell_length)
	r.Y=np.arange(ymin,ymax+cell_length,cell_length)
	r.nx=len(r.X)
	r.ny=len(r.Y)
	r.xllcorner=xllcorner
	r.yllcorner=yllcorner
	return r

def from_raster(raster,cell_length=None):
	"""
	Copy a raster without the data, optionnaly change the cell_length (=remap the raster)
	"""
	r=copy.deepcopy(raster)
	r.data={}
	if(cell_length is not None and cell_length!=raster.cell_length):
		r.cell_length=cell_length
		r.X=np.arange(raster.X[0],raster.X[-1]+cell_length,cell_length)
		r.Y=np.arange(raster.Y[0],raster.Y[-1]+cell_length,cell_length)
		r.nx=len(r.X)
		r.ny=len(r.Y)
		if "Z" in raster.data.keys():
			from skimage.transform import resize
			r.data["Z"]=resize(raster.data["Z"],[r.nx,r.ny])
	elif "Z" in raster.data.keys():
		r.data["Z"]=copy.deepcopy(raster.data["Z"])
	return r

def from_asc(filename, data_name, min_value=None):
	r=Raster()
	source_ds = gdal.Open(filename)
	r.nx = source_ds.RasterXSize
	r.ny = source_ds.RasterYSize
	xmin,Csize_x,a,ymax,b,Csize_y = source_ds.GetGeoTransform()
	ymin = ymax+r.ny*Csize_y
	r.cell_length = Csize_x
	r.xllcorner=xmin
	r.yllcorner=ymin
	band = source_ds.GetRasterBand(1)
	band.format = format(gdal.GetDataTypeName(band.DataType))
	data = band.ReadAsArray()
	nodata = band.GetNoDataValue()
	if nodata is None:
		nodata = data.min()
	data[np.isnan(data)]=nodata
	if min_value is not None:
		data[data<=min_value]=nodata
	data = np.flip(data.T, axis=1) #conversion between ASC coordinates to PlatRock coordinates (transpose then flip)
	source_ds.FlushCache()
	r.header_data={
		"cellsize":r.cell_length,
		"NODATA_value":nodata,
		"xllcorner":r.xllcorner,
		"yllcorner":r.yllcorner,
		"ncols":r.nx,
		"nrows":r.ny
	}
	r.X=np.arange(0,r.nx)*r.cell_length
	r.Y=np.arange(0,r.ny)*r.cell_length
	#store in raster data:
	r.data[data_name]=data
	return r
	
class Raster(object):
	def __init__(self):
		self.X=None
		self.Y=None
		self.nx=None
		self.ny=None
		self.cell_length=None
		self.xllcorner=None
		self.yllcorner=None
		self.data={}
	
	def get_indices_from_coords(self,coords):
		#coords must be np.array([x,y])
		indices_coords=(np.floor(coords/self.cell_length)).astype(int)					#indices of the cell ([xi,yi])
		return indices_coords
	
	def get_cell_ll_coords(self, ix_iy):
		return np.array([ix_iy[0]*self.cell_length,ix_iy[1]*self.cell_length], dtype=float)

	def ix_iy_is_inside(self, ix_iy):
		return (
			ix_iy[0] >= 0 and
			ix_iy[1] >= 0 and
			ix_iy[0] < self.nx and
			ix_iy[1] < self.ny
		)
	
	def is_scalar_type(self,name):
		try:
			len(self.data[name][0,0])
			return False
		except Exception:
			return True
	
	def get_scalar_fields(self):
		return [f for f in self.data.keys() if self.is_scalar_type(f)]
	
	def get_vector_fields(self):
		return [f for f in self.data.keys() if not self.is_scalar_type(f)]
	
	def add_data_grid(self,name,type,default_value=0):
		self.data[name]=np.empty([self.nx,self.ny],dtype=type)
		if(type==list):
			for i in range(np.shape(self.data[name])[0]):
				for j in range(np.shape(self.data[name])[1]):
					self.data[name][i,j]=[]
		else:
			self.data[name].fill(default_value)
		return self.data[name]
	
	def get_asc_header_string(self):
		values={"ncols":int(self.nx),
				"nrows":int(self.ny),
				"xllcorner":int(self.xllcorner),
				"yllcorner":int(self.yllcorner),
				"cellsize":self.cell_length,
				"NODATA_value":self.header_data["NODATA_value"]
				}
		S=""
		for k in values:
			S+=str(k).ljust(14)+str(values[k])+"\n"
		return S
	
	def output_to_asc(self,output_to_string=False,fields=None):
		if not fields:
			fields=self.get_scalar_fields()
		class output_buff():
			def __init__(self):
				self.buff=""
			def write(self,what):
				self.buff+=what
			def __repr__(self):
				return self.buff

		outputs={}
		for fi in fields:
			if(output_to_string):
				outputs[fi]=output_buff()
			else:
				outputs[fi]=open(str(fi)+".asc",'w')
			outputs[fi].write(self.get_asc_header_string())
			np.savetxt(outputs[fi], np.flip(self.data[fi],axis=1).T, fmt="%.2f")	#flip and transpose to translate from numpy representation to ascii grid representation
			if(output_to_string):
				outputs[fi]=outputs[fi].buff
			else:
				outputs[fi].close()
		if(output_to_string):
			return outputs















