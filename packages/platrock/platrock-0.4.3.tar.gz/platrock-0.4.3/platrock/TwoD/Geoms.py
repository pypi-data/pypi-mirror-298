"""
This module is used by the TwoD model. It describes 2D geometric objects and provide some functions to solve geometric problems.
"""

import numpy as np
import platrock.Common.Debug as Debug
import platrock.Common.Math as Math

class Parabola(object):
	"""
	A 2D parabola, described by : :math:`z = Ax^2 + Bx +C`. The instanciation can be done with either from:
	
	* :math:`g` and the velocity and position of a :class:`TwoD.Objects.Rock`,
	* :math:`g` and an explicit pair of position and velocity,
	* directly from an ABC vector/list.
	
	Args:
		r (:class:`TwoD.Objects.Rock`, optional): a rock from which to deduce the parabola
		pos (iterable, optional): a position in a list, a vector or an array :math:`[px, pz]`
		vel (iterable, optional): a velocity in a list, a vector or an array :math:`[vx, pz]`
		g (float, optional): the gravity acceleration
		ABC (iterable, optional): the A, B and C constants in a list, a vector or an array :math:`[A, B, C]`
		
	Attributes:
		A (float): the :math:`A` square parameter
		B (float): the :math:`B` linear parameter
		C (float): the :math:`C` constant parameter
		
	"""
	def __init__(self,r=None,pos=None,vel=None,g=None,ABC=None): #r is a rock
		if(not r==None):
			x=r.pos[0] ; y=r.pos[1]
			vx=r.vel[0] ; vy=r.vel[1]
		elif(isinstance(pos,Math.Vector2) and isinstance(vel,Math.Vector2)):
			x=pos[0] ; y=pos[1]
			vx=vel[0] ; vy=vel[1]
		elif(ABC is not None):
			self.A=ABC[0]
			self.B=ABC[1]
			self.C=ABC[2]
			return
		self.A=-g/(2.*vx**2)
		self.B=vy/vx+g*x/vx**2
		self.C=y-g*x**2/(2.*vx**2)-vy*x/vx
	
	def get_value_at(self,x):
		"""
		Returns the :math:`z` value of the parabola at the given :math:`x` position.
		
		Args:
			x (float): the :math:`x` value
			
		Returns:
			float: :math:`Ax^2 + Bx +C`
		"""
		return self.A*x*x + self.B*x + self.C
	
	def get_arrow_x_from_gradient(self,gradient):
		"""
		Returns the :math:`x` value of the arrow for this parabola and a slope defined by its gradient. If the parabola is a trajectory, the arrow is the highest (vertical) height of the object during its fly over the slope.
		
		Args:
			gradient (float): the slope gradient (:math:`dx/dy`)
			
		Returns:
			float: :math:`x_{arrow}`
		"""
		return (gradient-self.B)/(2*self.A)



class Line(object):
	"""
	A line, described by the two constants :attr:`a` and :attr:`b` in :math:`z=ax + b`. The instanciation can be done with either from:
	
	* a segment S
	* a and b constants
	* [x, y] of a point and a positive angle in radians
	
	Args:
		S (:class:`TwoD.Objects.Segment`, optional): a segment from which to deduce the line.
		
	Attributes:
		a (float): the rate of increase coefficient.
		b (float): the y-intercept.
	"""
	EPS = 1e-10
	def __init__(self,S=None,a=None,b=None,point=None,angle=None):
		self._vertical = False
		self._vertical_x = None
		self._horizontal = False
		if(not S==None):
			if(abs(S.points[0,0]-S.points[1,0])<self.EPS):
				self._vertical = True
				self._vertical_x = S.points[0,0]
				self.a = None
				self.b = None
			else:
				self.a=S.slope_gradient
				self.b=S.points[0,1]-(self.a*S.points[0,0])
		elif((not a==None) and (not b==None)):
			self.a=a
			self.b=b
		elif((isinstance(point, np.ndarray)) and (not angle==None) and (len(point)==2)):
			angle = angle%np.pi
			if(abs(angle-np.pi/2)<self.EPS or abs(angle-3*np.pi/2)<self.EPS):
				self._vertical = True
				self._vertical_x = point[0]
				self.a = None
				self.b = None
			else: #general case :
				self.a = np.tan(angle)
				self.b = point[1]-(self.a*point[0])
		if (self.a==0):
			self._horizontal = True

def get_roots(A,B,C):
	"""
	Gives the roots of the second order equation :math:`z=Ax^2 + Bx + C`. If there is no solutions, the returned array is empty. If the there is one solution only, it will be duplicated in the output array.
			
	Args:
		A (float): the square coefficient
		B (float): the linear coefficient
		C (float): the constant coefficient
	
	Returns:
		:class:`~platrock.Common.Math.Vector2`: array containing the two roots :math:`[x_{root1}, x_{root2}]`, or empty array.
	"""
	D=B*B-4.*A*C
	if(D<0.):
		return np.array([])
	else:
		D=np.sqrt(D)
		return Math.Vector2([(-B+D)/(2.*A),(-B-D)/(2.*A)])

def get_line_parabola_intersections(L,P):
	"""
	Computes the intersections between a line and a parabola. If no solutions, return a NaN-filled array.
	
	Args:
		L (:class:`TwoD.Geoms.Line`): the line
		P (:class:`TwoD.Geoms.Parabola`): the parabola
	
	Returns:
		:class:`numpy.ndarray`: the two solutions :code:`[[x_i1,z_i1], [x_i2, z_i2]]`:
	"""
	if(L._vertical):
		return np.array([[L._vertical_x,P.get_value_at(L._vertical_x)],[np.nan,np.nan]])
	else:
		roots = get_roots(P.A,P.B-L.a,P.C-L.b)	#The roots are the x-coords of the intersection(s). They are the solutions of the 2nd order polynom coming from : parabola_equation = line_equation.
		if(len(roots)>0):	#If the solution(s) exists
			return np.array([ [roots[0],L.a*roots[0]+L.b], [roots[1],L.a*roots[1]+L.b] ])
		return np.array([[np.nan,np.nan],[np.nan,np.nan]])	#No solutions

def get_segment_parabola_intersections(S,P):
	"""
	Computes the intersection(s) between a segment and a parabola. If no solutions, return an empty array.
	
	Args:
		S (:class:`TwoD.Objects.Segment`): the segment
		P (:class:`TwoD.Geoms.Parabola`): the parabola
		
	Returns:
		:class:`numpy.ndarray`: the eventual solutions :code:`[[x_i1, z_i1], [x_i2, z_i2]]`.
	"""
	potential_intersections=get_line_parabola_intersections(Line(S),P)
	valid_ids=[]
	for i in [0,1]:
		if(potential_intersections[i,0]>S.points[0,0] and potential_intersections[i,0]<S.points[1,0]):
			valid_ids.append(i)
	return potential_intersections[valid_ids]


def find_next_bounce(sim,rock,rock_parabola):
	"""
	In a given simulation, for a given rock, find the next rebound on the soil. The algorithm works as follows:
	
	#. compute the rock parabola
	#. loop on the segments from the :attr:`TwoD.Objects.Rock.current_segment` in the :attr:`TwoD.Objects.Rock.flying_direction`, and try to find a parabola-segment intersection
	#. keep the intersection with the soil if it is compatible with the rock flying direction and if it does not correspond to the previous rock rebound point
	
	Args:
		sim (:class:`TwoD.Simulations.Simulation`): the simulation
		rock (:class:`TwoD.Objects.Rock`): the rock
		
	Returns:
		(:class:`~platrock.Common.Math.Vector2` :code:`[x_i, z_i]`, :class:`TwoD.Objects.Segment`) : (intersection point, corresponding segment)
	"""
	Debug.info("Find next bounce")
	trying_segt=rock.current_segment
	#LOOP ON SEGMENTS#
	while(True):
	#for l in range(0,10):
		Debug.info("Trying to find rebound on segment n",trying_segt.index)
		intersections=get_segment_parabola_intersections(trying_segt,rock_parabola)
		Debug.info("Potential intersections:",intersections)
		#LOOP ON POTENTIAL INTERSECTIONS#
		for i in intersections:
			delta_x=i[0]-rock.pos[0]
			if(np.sign(delta_x)==rock.flying_direction and abs(delta_x)>1e-7):
				Debug.info("Keep intersection:",i,"with delta_x:",delta_x)
				return Math.Vector2(i),trying_segt #WE FOUND, SO STOP HERE
			else:
				Debug.info("Invalid intersection:",i,"with delta_x:",delta_x)
				continue #GO TO THE NEXT INTERSECTION, IF ANY
		#NO VALID INTERSECTION, GO TO NEXT SEGMENT
		ID=trying_segt.index+rock.flying_direction
		if(ID<0 or ID>len(sim.terrain.segments)-1):
			raise("find_next_bounce(): no intersection could be found for this rock on the whole terrain.")
		trying_segt=sim.terrain.segments[ID]
		Debug.info("No valid intersection found")
