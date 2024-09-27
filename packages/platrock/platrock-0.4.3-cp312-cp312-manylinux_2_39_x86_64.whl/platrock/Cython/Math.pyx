"""
Cython module intented to do mathematical operations as fast as possible.
"""

#cython: language_level=3, boundscheck=False, wraparound=False

import numpy as np
import quaternion
from libc.math cimport sin,cos,sqrt
from scipy.stats import gamma
import math

class Vector1(np.ndarray):	#this code derives from the numpy doc for subclassing np.ndarray.
	"""
	Mainly for defining angular velocity in 2D models, and still allows for computations while sharing bounce models between 2D and 3D models. Instanciation follows `numpy.ndarray` directives.
	"""
	def __new__(subtype, input=0.0):
		obj = super(Vector1, subtype).__new__(subtype, 1, float,None,0,None,None)
		if(np.isscalar(input)):
			obj[0]=input
			return obj
		else:
			obj[0]=input[0]
			return obj
	
	def dot(double[:] A,double[:] B):
		"""
		Get the dot product of this :class:`Vector1` by `B`, equivalent to regular scalar product.
		
		Args:
			B (:class:`~Vector1`)
		
		Returns:
			float
		"""
		return A[0]*B[0]
		
	def norm(double[:] A):
		"""
		Get the norm of this :class:`Vector1`, equivalent to absolute value.
		
		Returns:
			float
		"""
		return sqrt(A[0]**2)
	
	def normalized(double[:] A):
		"""
		Get the corresponding normalized :class:`Vector1`.
		
		Returns:
			:class:`Vector1`
		"""
		cdef double norm = sqrt(A[0]**2)
		return Vector1([A[0]/norm])
	
#NOTE: bind the Vector1 methods outside the class so that they can be used by PlatRock without instanciating a Vector1 object.
dot1=Vector1.dot
normalized1=Vector1.normalized
norm1=Vector1.norm

class Vector2(np.ndarray):
	"""
	Two components vector with fast operations, also allows for computations while sharing bounce models between 2D and 3D models. Instanciation follows `numpy.ndarray` directives.
	"""
	def __new__(subtype, input=[0,0]):
		assert(len(input)==2)
		obj = super(Vector2, subtype).__new__(subtype, 2, float,None,0,None,None)
		obj[0]=input[0]
		obj[1]=input[1]
		return obj
	
	def dot(double[:] A,double[:] B):
		"""
		Get the dot product of this :class:`Vector2` by `B`.
		
		Args:
			B (:class:`Vector2`)
		
		Returns:
			float
		"""
		return A[0]*B[0]+A[1]*B[1]
		
	def cross(double[:] A,double[:] B):
		"""
		Get the cross product of this :class:`Vector2` by `B`.
		
		Args:
			B (:class:`Vector2`)
		
		Returns:
			:class:`Vector1`
		"""
		return Vector1(A[0]*B[1]-A[1]*B[0])

	def norm(double[:] A):
		"""
		Get the norm of this :class:`Vector2`.
		
		Returns:
			float
		"""
		return sqrt(A[0]**2+A[1]**2)
	
	def normalized(double[:] A):
		"""
		Get the corresponding normalized :class:`Vector2`.
		
		Returns:
			:class:`Vector2`
		"""
		cdef double norm = sqrt(A[0]**2+A[1]**2)
		return Vector2([A[0]/norm,A[1]/norm])

	def rotated(double[:] A,double ang,ax=None):
		"""
		Get a rotated version of this :class:`Vector2`.
		
		Args:
			ang (float): the amount (angle) of rotation in radians.
			ax (None): not used, just here for compatibility with :class:`Vector3` operations
			
		Returns:
			:class:`Vector2`
		"""
		cdef double c=cos(ang)
		cdef double s=sin(ang)
		return Vector2([A[0]*c - A[1]*s , A[0]*s + A[1]*c])
	
#NOTE: bind the Vector2 methods outside the class so that they can be used by PlatRock without instanciating a Vector2 object.
cross2=Vector2.cross
dot2=Vector2.dot
normalized2=Vector2.normalized
rotated2=Vector2.rotated
norm2=Vector2.norm

class Vector3(np.ndarray):
	"""
	3 components vector with fast operations, also allows for computations while sharing bounce models between 2D and 3D models. Instanciation follows `numpy.ndarray` directives.
	"""
	def __new__(subtype, input=[0,0,0]):
		assert(len(input)==3)
		obj = super(Vector3, subtype).__new__(subtype, 3, float,None,0,None,None)
		obj[0]=input[0]
		obj[1]=input[1]
		obj[2]=input[2]
		return obj
	
	def normalized(A):
		"""
		Get the corresponding normalized :class:`Vector3`.
		
		Returns:
			:class:`Vector3`
		"""
		try:
			return A/norm3(A)
		except:
			return A*0.
	
	def norm(A):
		"""
		Get the norm of this :class:`Vector3`.
		
		Returns:
			float
		"""
		return np.sqrt(A[0]**2+A[1]**2+A[2]**2)
	
	def dot(A,B):
		"""
		Get the dot product of this :class:`Vector3` by `B`.
		
		Args:
			B (:class:`Vector3`)
		
		Returns:
			float
		"""
		return A[0]*B[0]+A[1]*B[1]+A[2]*B[2]
	
	def cross(A,B):
		"""
		Get the cross product of this :class:`Vector3` by `B`.
		
		Args:
			B (:class:`Vector3`)
		
		Returns:
			:class:`Vector3`
		"""
		return Vector3([A[1]*B[2]-A[2]*B[1],A[2]*B[0]-A[0]*B[2],A[0]*B[1]-B[0]*A[1]])
	
	def rotated(A,ang,ax):
		"""
		Get a rotated version of this :class:`Vector3`.
		
		Args:
			ang (float): the amount (angle) of rotation in radians.
			ax (:class:`Vector3`): the axis to turn around.
			
		Returns:
			:class:`Vector3`
		"""
		output_xyz=Vector3()
		c=np.cos(ang)
		s=np.sin(ang)
		ax=ax.normalized()
		output_xyz[0]=A[0]*( ax[0]**2*(1.-c)+c )             +     A[1]*( ax[0]*ax[1]*(1-c)-ax[2]*s )    +     A[2]*( ax[0]*ax[1]*(1-c)+ax[1]*s )
		output_xyz[1]=A[0]*( ax[0]*ax[1]*(1-c)+ax[2]*s )     +     A[1]*( ax[1]**2*(1-c)+c )             +     A[2]*( ax[1]*ax[2]*(1-c)-ax[0]*s )
		output_xyz[2]=A[0]*( ax[0]*ax[2]*(1-c)-ax[1]*s )     +     A[1]*( ax[1]*ax[2]*(1-c)+ax[0]*s )    +     A[2]*( ax[2]**2*(1-c)+c )
		return output_xyz

#Binds:
cross3=Vector3.cross
dot3=Vector3.dot
normalized3=Vector3.normalized
rotated3=Vector3.rotated
norm3=Vector3.norm


#For some reason, if the following isn't done, jsonpickle will load Vector2 and Vector3 as np.ndarray. (saving is okay by default)
import jsonpickle.handlers
import jsonpickle.ext.numpy
class _VectorJsonPickeHandler(jsonpickle.ext.numpy.NumpyNDArrayHandler):
	def __init__(self, *args,**kwargs):
		super(_VectorJsonPickeHandler,self).__init__(*args,**kwargs)
	def restore(self,data):
		obj=super(_VectorJsonPickeHandler,self).restore(data)
		if(len(obj)==1):
			return Vector1(obj)
		elif(len(obj)==2):
			return Vector2(obj)
		elif(len(obj)==3):
			return Vector3(obj)
jsonpickle.handlers.register(Vector1, _VectorJsonPickeHandler)
jsonpickle.handlers.register(Vector2, _VectorJsonPickeHandler)
jsonpickle.handlers.register(Vector3, _VectorJsonPickeHandler)


def rotate_vector(q,A):
	"""
	Get a rotated quaternion from an input quaternion q with a rotation vector A.
	
	Args:
		q (:class:`quaternion`): the quaternion to turn
		A (:class:`Vector3`): the rotation vector
	
	Returns:
		:class:`quaternion`
	"""
	return A + 2.*cross3(q.vec,(q.w*A+cross3(q.vec,A)))/(q.w**2+q.x**2+q.y**2+q.z**2)
quaternion.rotate_vector=rotate_vector


def atan2_unsigned(y,x):
	"""
	Returns atan2, but shifted in the interval [:math:`0`, :math:`2\pi`].
	
	Args:
		y (float)
		x(float)
	
	Returns:
		float
	"""
	value=math.atan2(y,x)
	if(value<0.):value+=2.*np.pi
	return value

def get_random_value_from_gamma_distribution(mean,std,rand_gen=None):
	"""
	Get a random value from a given gamma distribution. Uses scipy.stats.
	
	Args:
		mean (float): the desired distribution mean
		std (float): the desired distribution standard deviation
		rand_gen(:class:`numpy.random.RandomState`, optional): the random generator, useful for simulations reproductibility.
		
	Returns:
		float
	"""
	if abs(std)<1e-5 : return mean
	return gamma.rvs((mean/std)**2,0,std**2/mean,size=None,random_state=rand_gen)

#from http://math.15873.pagesperso-orange.fr/page9.htm
def get_2D_polygon_center_of_mass(points):
	"""
	From a 2D array of points forming a polygon, get its center of mass.
	
	Note:
		Taken from http://math.15873.pagesperso-orange.fr/page9.htm
	
	Args:
		points (:class:`numpy.ndarray`): the array of points forming the polygon in the form [[x0, y0], [x1, y1], ...]
	
	Returns:
		list: the center of mass coordinates :math:`[G_x, G_y]`
	"""
	area=Gx=Gy=0
	for i in range(-1,len(points)-1,1):
		interm=points[i][0]*points[i+1][1]-points[i+1][0]*points[i][1]
		area+=interm
		Gx+=(points[i][0]+points[i+1][0])*interm
		Gy+=(points[i][1]+points[i+1][1])*interm
	area*=0.5
	Gx/=6*area
	Gy/=6*area
	return [Gx,Gy]
	
def get_2D_polygon_area_inertia(points,density,cog_centered=False):
	"""
	From a 2D array of points forming a polygon, get its area and inertia.

	Args:
		points (:class:`numpy.ndarray`): the array of points forming the polygon in the form [[x0, y0], [x1, y1], ...]
		density (float): the 2D polygon density, used to compute inertia
		cog_centered (bool, optional): whether the polygon COG in also at coordinates [0,0] or not.
	
	Returns:
		list: the area and inertia, :math:`[A, I]`.
	"""
	if(not cog_centered):
		#Get the COG
		cog = get_2D_polygon_center_of_mass(points)
		#Center the polygon to the COG (so set COG to (0,0))
		centered_points = points[:] - cog
	else:
		centered_points=points
	#Loop on triangles around the COG (0,0) and compute its inertia
	I=0; A=0
	for i in range(-1,centered_points.shape[0]-1):
		B=Vector2(centered_points[i])
		C=Vector2(centered_points[i+1])
		tri_area=(B.cross(C)).norm()/2
		A+=tri_area
		I+=tri_area/6 * ( B.dot(B) + B.dot(C) + C.dot(C) )
	return [A,I*density]

def sort_2d_polygon_vertices(points):
	"""
	Sort in place a 2D array of points to form a polygon.

	Args:
		points (:class:`numpy.ndarray`): the array of points in the form [[x0, y0], [x1, y1], ...]
	"""
	center=points.mean(axis=0)
	points[:]=points-center
	atan2_list=np.asarray([atan2_unsigned(p[1],p[0]) for p in points])
	points[:]=points[atan2_list.argsort()]+center
	
	
def center_2d_polygon_vertices(points):
	"""
	Move in place a 2D array of points forming a polygon to set its COG to [0,0].

	Args:
		points (:class:`numpy.ndarray`): the array of points forming the polygon in the form [[x0, y0], [x1, y1], ...]
	"""
	points[:]-=get_2D_polygon_center_of_mass(points)

def rotate_points_around_origin(points,radians):
	"""
	Rotate in place a 2D array of points around [0,0].

	Args:
		points (:class:`numpy.ndarray`): the array of points in the form [[x0, y0], [x1, y1], ...]
		radians (float): the amount of rotation, (angle in radians)
	"""
	
	pointsX = points[:,0]*np.cos(radians) - points[:,1]*np.sin(radians)
	pointsY = points[:,0]*np.sin(radians) + points[:,1]*np.cos(radians)
	points[:] = np.array([pointsX,pointsY]).transpose()
	
def get_random_convex_polygon(n,Lx,Ly):
	"""
	Get a random convex 2D array of points forming a polygon.
	
	Note:
		Valtr's algorithm is used, it can be found here : https://cglab.ca/~sander/misc/ConvexGeneration/convex.html
	
	Args:
		n (int): the number of vertices
		Lx (float): the polygon size in the :math:`x` direction
		Ly (float): the polygon size in the :math:`y` direction
	Returns:
		:class:`numpy.ndarray`: 2D array of points forming the polygon
	"""
	xPool = np.sort(np.random.rand(n))
	yPool = np.sort(np.random.rand(n))

	minX=xPool[0]
	maxX=xPool[-1]
	minY=yPool[0]
	maxY=yPool[-1]

	xVec = np.zeros(n)
	yVec = np.zeros(n)
	lastTop = minX
	lastBot = minX
	for i in range(1,n-1):
		x = xPool[i]
		if np.random.random()>0.5 :
			xVec[i-1]=x - lastTop
			lastTop = x
		else:
			xVec[i-1]=lastBot - x
			lastBot = x
	xVec[-2]=maxX - lastTop
	xVec[-1]=lastBot - maxX

	lastLeft = minY
	lastRight = minY
	for i in range(1,n-1):
		y = yPool[i]
		if np.random.random()>0.5 :
			yVec[i-1]=y - lastLeft
			lastLeft = y
		else:
			yVec[i-1]=lastRight - y
			lastRight = y
	yVec[-2]=maxY - lastLeft
	yVec[-1]=lastRight - maxY

	np.random.shuffle(yVec)
	vec=np.array((xVec,yVec)).transpose()
	
	angles=np.arctan2(vec[:,1],vec[:,0])
	vec=vec[angles.argsort()]

	vec[:,0]=np.cumsum(vec[:,0])
	vec[:,1]=np.cumsum(vec[:,1])
	
	xShift=minX - vec[:,0].min() - 0.5
	yShift=minY - vec[:,1].min() - 0.5
	
	vec+=np.array([xShift,yShift])
	
	# End of Valtr's algorithm
	
	#Find the largest point-point distance:
	maxDist=-np.inf
	id1=-1 ; id2=-1
	for i in range(n):
		for j in range(i+1,n):
			d=Vector2(vec[i]-vec[j]).norm()
			if(d>maxDist):
				maxDist=d
				id1=i ; id2=j
	
	#Find the angle of the largest point-point distance:
	long_vect = vec[id1]-vec[id2]
	angle = - np.arctan2(long_vect[1],long_vect[0])
	
	#Rotate the polygon to align its principal axis with X
	rotate_points_around_origin(vec,angle)
	
	#Scale with Lx and Ly:
	DX=vec[:,0].max() - vec[:,0].min()
	DY=vec[:,1].max() - vec[:,1].min()
	vec[:,0] *= Lx/DX
	vec[:,1] *= Ly/DY

	return vec


















