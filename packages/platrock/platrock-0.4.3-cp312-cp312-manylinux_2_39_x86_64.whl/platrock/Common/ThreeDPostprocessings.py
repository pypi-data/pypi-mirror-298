"""
"""

# TODO: forest integration 
import numpy as np
#from . import Objects
import platrock.Common.Math as Math
from . import RasterTools
from platrock.Common import Outputs


class ThreeDPostprocessing(object):
	def __init__(self,simulation,raster_cell_length=None):
		self.simulation=simulation
		self.has_run=False
		if raster_cell_length is not None:
			raster_cell_length = float(raster_cell_length)
		self.raster=RasterTools.from_raster(simulation.terrain.Z_raster,cell_length=raster_cell_length)
		self.simulation.pp=self
		self.current_rock_id = -1
	
	def get_indices_cleaned(self,arr):
		arr_shift1=np.roll(arr,1,axis=0)
		arr_shift2=np.roll(arr,-1,axis=0)
		XCompare=np.where(arr_shift1[:,0]!=arr_shift2[:,0])[0]
		YCompare=np.where(arr_shift1[:,1]!=arr_shift2[:,1])[0]
		# ensure to always output the first and the last contacts
		# (the above algo exclude them if the first and the last contacts are in the same cell) 
		XCompare=np.insert(XCompare,0,0)
		XCompare=np.append(XCompare,arr.shape[0]-1)
		return np.unique( np.concatenate((XCompare,YCompare)) )
	
	def get_raster_indices_from_contacts(self,c_pos,c_types):
		# Len=np.sum(c_types!=Outputs.OUT) # exclude out of bounds contacts as it will likely give cells indices outside raster.
		Len = len(c_types)
		raster_indices=np.empty([Len,2],dtype=int)
		for i in range(Len):
			raster_indices[i]=self.raster.get_indices_from_coords(c_pos[i,0:2])
		return raster_indices
	
	def insert_fly(self,arrays_dict,where):
		for k in arrays_dict.keys():
			arrays_dict[k]=np.insert(arrays_dict[k],where,np.zeros(arrays_dict[k][0].shape),axis=0)
		arrays_dict["pos"][where]=arrays_dict["pos"][where-1]	#in the case of a flight, pos and vel are copied from the last known contact
		arrays_dict["vels"][where]=arrays_dict["vels"][where-1]
		arrays_dict["types"][where]=Outputs.FLY
		arrays_dict["angVels"][where]=arrays_dict["angVels"][where-1]
	
	def delete_overflowing_raster_indices_and_contacts(self, raster_indices, all_c_fields):
		indices_to_be_removed = []
		for i, ix_iy in enumerate(raster_indices):	#loop on all cells the rocks passed over
			if (
				ix_iy[0] < 0 or
				ix_iy[1] < 0 or
				ix_iy[0] >= self.raster.nx or
				ix_iy[1] >= self.raster.ny
			):
				indices_to_be_removed.append(i)
		raster_indices = np.delete(raster_indices, indices_to_be_removed, axis=0)
		for k in all_c_fields.keys():
			all_c_fields[k] = np.delete(all_c_fields[k], indices_to_be_removed, axis=0)
		return (raster_indices,all_c_fields)

			
	def add_flights_to_raster_cells_and_contacts(self, raster_indices, all_c_fields):
		# A new contact type is now added : flights_over_cells
		#DETECT FLYING (contactless) CELLS ON THE RASTER :
		i=0
		while i < len(raster_indices)-1:
			ix, iy = raster_indices[i,0], raster_indices[i,1]
			ix_next, iy_next=raster_indices[i+1,0], raster_indices[i+1,1]
			#print("Raster indices :",[ix, iy],"=>",[ix_next, iy_next],"|",all_c_fields["pos"][i][0:2],'=>',all_c_fields["pos"][i+1][0:2] ,end='')
			cells_indices_distance=abs(ix_next-ix) + abs(iy_next-iy) # -> how far are the cells if I only jump through the cells edges (no diagonals) ?
			if(cells_indices_distance<=1): # consecutive contacts on the same raster cell (=0), or consecutive contacts on neighbours raster cell (=1)
				i+=1
				#print(' (CONTINUOUS)')
				continue
			else:	#a fly occured : complete the rock path on the raster with flying cells
				current_pos=all_c_fields["pos"][i][0:2]
				start_pos=current_pos[:]
				rock_branch=Math.Vector2(all_c_fields["pos"][i+1][0:2]-current_pos)
				#print(' (FLY, rock_branch=',rock_branch,')')
				ix2=ix ; iy2=iy
				flies_counter = 0
				while(abs(ix_next-ix2) + abs(iy_next-iy2)>1): #while we didn't reached a neighbour of the next contact cell ...
					assert flies_counter < 1000
					flies_counter+=1
					#print('    current_pos =',current_pos,'[ix2, iy2] =',[ix2, iy2],end='')
					EPS = 1e-10
					if abs(rock_branch[0])-EPS < 0 :
						if rock_branch[1] > 0:
							current_pos=start_pos+rock_branch*((self.raster.get_cell_ll_coords([0,iy2+1])[1]-start_pos[1])/rock_branch[1])
							iy2+=1
						else:
							current_pos=start_pos+rock_branch*((self.raster.get_cell_ll_coords([0,iy2])[1]-start_pos[1])/rock_branch[1])
							iy2-=1
					elif abs(rock_branch[1])-EPS < 0 :
						if rock_branch[0] > 0:
							current_pos=start_pos+rock_branch*((self.raster.get_cell_ll_coords([ix2+1,0])[0]-start_pos[0])/rock_branch[0])
							ix2+=1
						else:
							current_pos=start_pos+rock_branch*((self.raster.get_cell_ll_coords([ix2,0])[0]-start_pos[0])/rock_branch[0])
							ix2-=1
					else:

						# GENERAL CASE: find a pair of cross products that comes from a pair of branch vectors that
						# surrounds the rock branch orientation. It means that
						# we are sure to know the following raster cell we should go to (see below).

						SE_branch=Math.Vector2(self.raster.get_cell_ll_coords([ix2+1, iy2])-current_pos)#South-East
						SW_branch=Math.Vector2(self.raster.get_cell_ll_coords([ix2, iy2])-current_pos)#South-West
						NW_branch=Math.Vector2(self.raster.get_cell_ll_coords([ix2, iy2+1])-current_pos)#North-West
						NE_branch=Math.Vector2(self.raster.get_cell_ll_coords([ix2+1, iy2+1])-current_pos)#North-East
						#print(' => General case | Branches: ↘',SE_branch,' ↙',SW_branch,' ↖',NW_branch,' ↗',NE_branch,sep='')

						SE_cross=rock_branch.cross(SE_branch)[0]
						SW_cross=rock_branch.cross(SW_branch)[0]
						NW_cross=rock_branch.cross(NW_branch)[0]
						NE_cross=rock_branch.cross(NE_branch)[0]

						if   (NE_cross>=0 and SE_cross<=0): # TOWARDS EAST
							current_pos=start_pos+rock_branch*((self.raster.get_cell_ll_coords([ix2+1,0])[0]-start_pos[0])/rock_branch[0])
							ix2+=1
						elif (NW_cross>=0 and NE_cross<=0): # TOWARDS NORTH
							current_pos=start_pos+rock_branch*((self.raster.get_cell_ll_coords([0,iy2+1])[1]-start_pos[1])/rock_branch[1])
							iy2+=1
						elif (SW_cross>=0 and NW_cross<=0): # TOWARDS WEST
							current_pos=start_pos+rock_branch*((self.raster.get_cell_ll_coords([ix2,0])[0]-start_pos[0])/rock_branch[0])
							ix2-=1
						elif (SE_cross>=0 and SW_cross<=0): # TOWARDS SOUTH
							current_pos=start_pos+rock_branch*((self.raster.get_cell_ll_coords([0,iy2])[1]-start_pos[1])/rock_branch[1])
							iy2-=1
					
					raster_indices=np.insert(raster_indices,i+1,[ix2,iy2],axis=0)
					self.insert_fly(all_c_fields,i+1)
					i+=1
				i+=1
		return (raster_indices,all_c_fields)

	def run(self):
		self.run_init()
		self.run_all_rocks()
		self.run_end()

	def run_init(self):
		self.raster.add_data_grid("crossings",int,0)
		self.raster.add_data_grid("heights",list)
		self.raster.add_data_grid("vels",list)
		self.raster.add_data_grid("stops_nb",int,0) #store the number of stops per cell
		self.raster.add_data_grid("stops_origin",list) #at each stop cell, store a list of START cell coordinates
		self.raster.add_data_grid("Ec",list) #Kinetic energy
		self.raster.add_data_grid("nb_trees_impacts",int,0)
		self.raster.add_data_grid("trees_impacts_max_height",float,0)
	
	def run_one_rock(self):
		self.current_rock_id += 1
		r_nb = self.current_rock_id
		print("PP for rock nb",r_nb)
		c_pos   = self.simulation.output.get_contacts_pos(r_nb)
		c_types = self.simulation.output.get_contacts_types(r_nb)
		c_tree_ids = np.where(np.logical_or(c_types==Outputs.TREE,c_types==Outputs.ROLL_TREE))[0]
		
		#find cells from contacts pos. raster_indices will be the consecutive list of raster indices the rock has crossed.
		raster_indices = self.get_raster_indices_from_contacts(c_pos,c_types)
		for tree_id in c_tree_ids:
			raster_id=raster_indices[tree_id]
			if self.raster.ix_iy_is_inside(raster_id) :
				height=c_pos[tree_id][2]-self.raster.data["Z"][raster_id[0],raster_id[1]]
				self.raster.data["nb_trees_impacts"][raster_id[0],raster_id[1]]+=1
				self.raster.data["trees_impacts_max_height"][raster_id[0],raster_id[1]]=max( self.raster.data["trees_impacts_max_height"][raster_id[0],raster_id[1]], height )
		self.ri_1 = raster_indices[:]
		#CLEANING PASS : when consecutive contacts on the same raster cell occurs, only keep the first one and the last one
		indices_duplicates_removed=self.get_indices_cleaned(raster_indices)
		raster_indices=raster_indices[indices_duplicates_removed]	# LIST OF RASTERS ON WHICH CONTACTS OCCURED
		c_pos=c_pos[indices_duplicates_removed]
		c_vels=self.simulation.output.get_contacts_vels(r_nb)[indices_duplicates_removed]
		c_types=c_types[indices_duplicates_removed]
		c_angVels=self.simulation.output.get_contacts_angVels(r_nb)[indices_duplicates_removed]
		all_c_fields={"pos":c_pos,"vels":c_vels,"types":c_types,"angVels":c_angVels}
		self.ri_2 = raster_indices[:]
		# add flights (cells with no contacts). Finally, len(raster_indices) == len(contacts), allowing to loop over both at the same time.
		raster_indices, all_c_fields = self.add_flights_to_raster_cells_and_contacts(raster_indices, all_c_fields)
		self.ri_3 = raster_indices[:]
		# At this time, no mechanism was applied to avoid raster_indices to be outside the raster domain. Do it now.
		raster_indices, all_c_fields = self.delete_overflowing_raster_indices_and_contacts(raster_indices, all_c_fields)
		self.ri_4 = raster_indices[:]
		# Count the number of rocks that passed over each cell :
		rock_count=np.zeros(np.shape(self.raster.data["crossings"]),dtype=int) #init to 0
		for index in raster_indices:	#loop on cells the rocks passed over
			rock_count[index[0],index[1]]+=1	#increment
		rock_count[rock_count>0]=1			#limit the value to 0 to avoid multiple rebounds on a single cell
		self.raster.data["crossings"]+=rock_count	#add this rock_count to the global data
		
		#Handle start cells:
		self.raster.data["heights"][raster_indices[0,0],raster_indices[0,1]].append(all_c_fields["pos"][0][2]-self.raster.data["Z"][raster_indices[0,0],raster_indices[0,1]]) #at this time, heights is in absolute coords
		self.raster.data["vels"][raster_indices[0,0],raster_indices[0,1]].append(np.linalg.norm(all_c_fields["vels"][0]))
		self.raster.data["Ec"][raster_indices[0,0],raster_indices[0,1]].append(
			0.5*(
				self.simulation.output.densities[r_nb]*self.simulation.output.volumes[r_nb]*np.linalg.norm(all_c_fields["vels"][0])**2 + #translation
				np.dot(all_c_fields["angVels"][0],np.dot(self.simulation.output.inertias[r_nb],all_c_fields["angVels"][0])) #rotation
			)
		)# See below to have a more explicit computation of Ec
		#Loop on raster indices (successive cells crossed by the rock) to fill output rasters.
		for i in range(1,len(raster_indices)): #FIXME : if a rock come back into a cell, avoid it
			index=raster_indices[i]
			prev_index=raster_indices[i-1]
			if((index==prev_index).all()): # if the previous contact was in the same cell, do nothing
				continue
			previous_c_pos=all_c_fields["pos"][i-1]
			previous_c_vel=all_c_fields["vels"][i-1]
			if(prev_index[1]-index[1] == 1):# the rock came to the current cell from the north face
				yM=self.raster.Y[prev_index[1]]	#the y coordinate of north face of the cell
				time=(yM-previous_c_pos[1])/previous_c_vel[1] # time = flight time from last effective contact to the entering of the rock in the cell
				xM=previous_c_vel[0]*time+previous_c_pos[0]
			elif(prev_index[1]-index[1] == -1): # the rock came to the current cell from the south face
				yM=self.raster.Y[index[1]]	#the y coordinate of south face of the cell
				time=(yM-previous_c_pos[1])/previous_c_vel[1]
				xM=previous_c_vel[0]*time+previous_c_pos[0]
			elif(prev_index[0]-index[0] == 1):	# the rock came to the current cell from the east face
				xM=self.raster.X[prev_index[0]] #the x coordinate of east face of the cell
				time=(xM-previous_c_pos[0])/previous_c_vel[0]
				yM=previous_c_vel[1]*time+previous_c_pos[1]
			elif(prev_index[0]-index[0] == -1): # the rock came to the current cell from the west face
				xM=self.raster.X[index[0]] #the x coordinate of the west face of the cell
				time=(xM-previous_c_pos[0])/previous_c_vel[0]
				yM=previous_c_vel[1]*time+previous_c_pos[1]
			if(np.isnan(time)):	# NOTE: this is for a very specific case, if the rebound occurs exactly on a cell edge and with vx=0 and/or vy=0.
				vel=Math.Vector3(all_c_fields["vels"][i])
				absolute_height=all_c_fields["pos"][i][2]
			else: # this is the general case
				absolute_height=-0.5*self.simulation.gravity*time**2 + previous_c_vel[2]*time + previous_c_pos[2] #FIXME : compute relative height
				vel=Math.Vector3([previous_c_vel[0], previous_c_vel[1], previous_c_vel[2] - self.simulation.gravity*time])
			
			self.raster.data["heights"][index[0],index[1]].append(absolute_height-self.raster.data["Z"][index[0],index[1]]) #heights will be relative
			self.raster.data["vels"][index[0],index[1]].append(vel.norm())
			#Compute Ec and add it the the raster cell:
			I=self.simulation.output.inertias[r_nb]
			angVel=all_c_fields["angVels"][i]
			density=self.simulation.output.densities[r_nb]
			volume=self.simulation.output.volumes[r_nb]
			Ec=0.5*( density*volume*vel.norm()**2 + np.dot(angVel,np.dot(I,angVel)) ) # mv² + ω_t X I X ω
			self.raster.data["Ec"][index[0],index[1]].append(Ec)
		
		#Handle stops:
		if(c_types[-1]==Outputs.STOP):
			self.raster.data["stops_nb"][index[0],index[1]]+=1
			self.raster.data["stops_origin"][index[0],index[1]].append(raster_indices[0])
		
	def run_all_rocks(self):
		for r_nb in range(self.simulation.nb_rocks):
			self.run_one_rock()
	
	def run_end(self):
		#Compute stats rasters based on other rasters:
		ids=np.where(self.raster.data["crossings"]!=0)
		for field in ["heights","vels", "Ec"]:
			#1- means:
			mean_raster_data=self.raster.add_data_grid(field+"_mean",float)
			for i,j in zip(*ids):
					mean_raster_data[i,j]=sum(self.raster.data[field][i,j])/len(self.raster.data[field][i,j])
			#2- quantiles:
			for quantile in [90,95,99]:
				quantiles_raster_data=self.raster.add_data_grid(field+"_quantile-"+str(quantile)+"%",float)
				for i,j in zip(*ids):
					quantiles_raster_data[i,j]=np.quantile(self.raster.data[field][i,j],quantile/100,interpolation="linear")
		
		raster_data=self.raster.add_data_grid("number_of_source-cells",int)
		for i in range(self.raster.nx):
			for j in range(self.raster.ny):
				Len=len(self.raster.data["stops_origin"][i,j])
				if Len>0:
					raster_data[i,j]=len(np.unique(self.raster.data["stops_origin"][i,j],axis=0))
		
		#Fill with NO_DATA where there was no rocks (for scalar data only):
		#(Note that we even modify "crossings" in the following)
		ids=np.where(self.raster.data["crossings"]==0)
		for field in self.raster.get_scalar_fields():
			if field=="Z" : continue
			self.raster.data[field][ids]=self.raster.header_data["NODATA_value"]
	
		self.has_run=True
	
	def plot(self):
		import platrock.GUI.Plot3D
		self.plot=platrock.GUI.Plot3D
