"""
Module that handles the generation of trees.
"""

import numpy as np

class OneDTreeGenerator():
	"""
	Computes the (1D) distance before the next tree impact from the trees/rock properties and a probability law. Instanciate then launch :meth:`getOneRandomTreeImpactDistance` to get the next distance.
	
	Note:
		The probability is constructed as follows. Trees are seen as layers of trees, randomly shifted at each layer but spaced regularly by a distance :math:`l` to satisfy the trees density. We compute :math:`q`, the probability to pass through one layer, which in turns gives the impact CDF as a function of the distance travelled by the rock :math:`x` : :math:`CDF(x)=1-q^{x/l}`. By defnition, the PDF is finally the derivative function of the CDF.
	
	Attributes:
		sim (:class:`~Common.Simulations.GenericSimulation`, optional): the parent simulation
		treesDensity (float): the trees density, in trees/m²
		trees_dhp (float, optional): the trees mean diameter, in meters
		dRock (float, optional): the rock equivalent diameter, in meters
		l (float): the computed virtual distance between two trees
		q (float): the probability to pass through 1 screen of trees without impact, i.e. to travel through :attr:`l` distance without impact
		prob0 (float): the probability to hit a tree immediately
		random_generator (): copied from simulation or :class:`numpy.random`
	"""
	def __init__(self,sim,treesDensity=0.1,trees_dhp=0.3,dRock=0.5):
		self.treesDensity = treesDensity
		self.trees_dhp = trees_dhp
		self.dRock = dRock
		self.sim=sim
		self._precomputeData()
		
	def _precomputeData(self):
		self.l=1/np.sqrt(self.treesDensity)				# virtual distance between two trees
		#p=(self.trees_dhp+self.dRock)/self.l 			# probability to hit a tree for 1 screen
		self.q=1-(self.trees_dhp+self.dRock)/self.l		# probability to pass through 1 screen of trees without impact, i.e. to travel through self.l distance without impact.
		self.prob0=self._PDF_impact(0)					# probability to hit a tree immediately
		if(self.sim==None):
			self.random_generator=np.random
		else:
			self.random_generator=self.sim.random_generator
	
	# NOTE: NOT USED, just for information.
	def _CDF_impact(self,x):
		return 1-self.q**(x/self.l)
	def _PDF_impact(self,x):
		return -(self.q**(x/self.l))/self.l * np.log(self.q)
	def getOneRandomTreeImpactDistance(self):
		"""
		Get the next impact distance from the instanciated object (pick a value from the previously computed PDF function).
		
		Returns:
			float
		"""
		random=self.prob0*self.random_generator.rand()
		return np.log(-random*self.l/np.log(self.q))*self.l/np.log(self.q)


