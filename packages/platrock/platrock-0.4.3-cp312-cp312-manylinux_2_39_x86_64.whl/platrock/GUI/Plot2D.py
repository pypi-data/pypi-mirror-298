"""
"""

import platrock
import numpy as np
import platrock.TwoD.Geoms as Geoms
import platrock.Common.Math as Math
import matplotlib as mpl
import plotly.offline as plyo
import plotly.graph_objs as plygo
import platrock.Common.ColorPalettes as cp
from platrock.Common import Outputs

if platrock.web_ui:
	mpl.use('Agg')
	#import plotly as ply
import matplotlib.pyplot as plt
if not platrock.web_ui: plt.ion()

mpl.rcParams["figure.subplot.bottom"]=0.04
mpl.rcParams["figure.subplot.top"]=0.99
mpl.rcParams["figure.subplot.left"]=0.03
mpl.rcParams["figure.subplot.right"]=0.99

fig=plt.figure("PlatRock 2D View",facecolor="w",edgecolor="w")
ax=plt.axes()

def clear():
	global fig,ax
	plt.close("all")
	fig=plt.figure("PlatRock 2D View",facecolor="w",edgecolor="w")
	ax=plt.axes()

def draw_terrain(t):
	seg_points=t.get_points()
	delta_z=max(seg_points[:,1])-min(seg_points[:,1])
	delta_x=max(seg_points[:,0])-min(seg_points[:,0])
	fig.set_size_inches( (18,int(18*1.8*delta_z/delta_x)), forward=True)
	ax.set_ylim(np.min(seg_points[:,1])-0.1*delta_z,np.max(seg_points[:,1])+0.1*delta_z)
	ax.set_xlim(np.min(seg_points[:,0])-0.01*delta_x,np.max(seg_points[:,0])+0.01*delta_x)
	ax.set_aspect("equal")
	ax.fill_between(seg_points[:,0],seg_points[:,1],color="#844200")
	fig.canvas.draw()

def plot_trajectory(s,rock_id,nb_points=10, draw=True, with_contacts=False, use_plotly=False):
	color=s.random_generator.rand(3)
	X=np.array([],dtype=float)
	Y=np.array([],dtype=float)
	pos=s.output.get_contacts_pos(rock_id)
	vels=s.output.get_contacts_vels(rock_id)
	types=s.output.get_contacts_types(rock_id)
	normals=s.output.get_contacts_normals(rock_id)
	if (types==Outputs.MOTION).any():
		for i in range(len(pos)-1):
			X=np.append(X,[pos[i][0]])
			Y=np.append(Y,[pos[i][1]])
	else:
		for i in range(len(pos)-1):
			if(types[i] in [Outputs.START,Outputs.SOIL,Outputs.TREE]): #parabola
				x=np.linspace(pos[i][0],pos[i+1][0],nb_points)
				X=np.append(X,x)
				P=Geoms.Parabola(pos=Math.Vector2(pos[i]),vel=Math.Vector2(vels[i]),g=s.gravity)
				Y=np.append(Y,P.A*x*x+P.B*x+P.C)
			elif(types[i]==Outputs.ROLL):
				x=[pos[i][0],pos[i+1][0]]
				X=np.append(X,x)
				y=[pos[i][1],pos[i+1][1]]
				Y=np.append(Y,y)
	pos_trees = pos[np.where((types==Outputs.TREE) | (types==Outputs.ROLL_TREE))[0]]
	trees_x=pos_trees[:,0]
	trees_y=pos_trees[:,1]
	if(use_plotly):
		return X,Y,np.asarray(trees_x),np.asarray(trees_y)
	ax.plot(X,Y,alpha=0.5,lw=2,color=color)
	if(with_contacts):
		for x,y in zip(trees_x,trees_y):
			ax.plot(trees_x,trees_y,"^",ms=7,color=color)
		if not((types==Outputs.MOTION).any()):
			for i in range(len(normals)):
				if(types[i] in [Outputs.START,Outputs.SOIL]):
					vect=Math.Vector2(normals[i]).rotated(-np.pi/2.)
					ax.plot([pos[i][0]-vect[0],pos[i][0]+vect[0]], [pos[i][1]-vect[1],pos[i][1]+vect[1]],"--",color=color)
	if(draw):
		fig.canvas.draw()

def plot_trajectories(s,rocks_ids, with_contacts=False):
	for i in rocks_ids:
		plot_trajectory(s,i,draw=False,with_contacts=with_contacts)
	fig.canvas.draw()

def plot_sample_trajectories(s,nb=10, with_contacts=False, use_plotly=False):
	rocks_to_plot=[]
	if(nb>=s.nb_rocks):
		rocks_to_plot=range(s.nb_rocks)
	else:
		rocks_to_plot=np.linspace(0,s.nb_rocks-1,nb,dtype=int)
	if not use_plotly:
		plot_trajectories(s,rocks_to_plot,with_contacts=with_contacts)
	else:
		#this will create [ [X_r1,Y_r1,Xtrees_r1,Ytrees_r1], [X_r2,Y_r2,Xtrees_r2,Ytrees_r2] ...]
		return [ plot_trajectory(s,i,use_plotly=True) for i in rocks_to_plot ]

def plot_checkpoints(s, with_crossings=False):
	z_range=s.terrain.get_z_range()
	z_range=z_range[1]-z_range[0]
	x_range=s.terrain.get_x_range()
	x_range=x_range[1]-x_range[0]
	max_range = max(x_range, z_range)
	style_kwargs = {'lw':4, 'alpha':0.4, 'color':'red'}
	for chkP in s.checkpoints:
		coords = chkP.get_plotting_coords(high_value=max_range)
		ax.plot(coords[:,0], coords[:,1], **style_kwargs)
		if(with_crossings and hasattr(chkP,"heights")):
			for i in range(len(chkP.heights)):
				cross_pos = chkP.base_point + chkP.dir_vect * chkP.heights[i]
				ax.arrow(cross_pos[0],cross_pos[1],chkP.vels[i][0],chkP.vels[i][1],head_width=2,head_length=2)
	fig.canvas.draw()

def get_plotly_raw_html(s, sample_trajectories=False):
	#Initialize the lists
	data = []
	annotations = []
	#1- plot the terrain:
	seg_points = s.terrain.get_points()
	terrain_dx=seg_points[:,0].max()-seg_points[:,0].min()
	terrain_dy=seg_points[:,1].max()-seg_points[:,1].min()
	bbox=[	#bounding box: [ minx, maxx, miny, maxy ]
		seg_points[:,0].min()-0.05*terrain_dx,
		seg_points[:,0].max()+0.05*terrain_dx,
		seg_points[:,1].min()-0.05*terrain_dy,
		seg_points[:,1].max()+0.05*terrain_dy,
	]
	
	i=0
	zones_polygon_centers=[]
	zones_polygon_colors=[]
	for zone in s.terrain.params_zones:
		zone_pts=seg_points[zone.start_id:zone.end_id+2,:]
		zones_polygon_centers.append(Math.get_2D_polygon_center_of_mass(np.append(zone_pts,[[zone_pts[-1,0],bbox[2]],[zone_pts[0,0],bbox[2]]],axis=0)))
		zones_polygon_colors.append(cp.color_to_html(zone["color"]))
		zero_line = plygo.Scatter(
			x=[zone_pts[0,0],zone_pts[-1,0]],
			y=[bbox[2]]*2,
			fill='none',
			line=dict(
					color="rgba(255,255,255,0)",
					width=0
			),
			hoverinfo='skip',
			mode="lines",
			name='zones'
		)
		terrain = plygo.Scatter(
			x=zone_pts[:,0],
			y=zone_pts[:,1],
			mode='lines+markers',
			fill='tonexty',
			text="Point",
			line=dict(
				color=zones_polygon_colors[-1],
				width=3
			),
			name='terrain',
			hoverinfo='text+x+y',
		)
		data.append(zero_line)
		data.append(terrain)
		i+=1
		
	#1.1- plot markers at zones centers to handle hoverinfo/clicks events
	zones_polygon_centers=np.asarray(zones_polygon_centers)
	data.append(plygo.Scatter(
		x=zones_polygon_centers[:,0],
		y=zones_polygon_centers[:,1],
		text = ["Zone "+str(i) for i in range(len(zones_polygon_centers))],
		mode = 'markers',
		marker = dict(
			symbol = 'circle',
			size = 15,
			color = zones_polygon_colors,
		),
		hoverinfo='text',
		name="zones"
	))
	
	#2- plot the checkpoints:
	for chkP in s.checkpoints:
		if (not chkP.init_data_done) :
			chkP.init_data(s)
		coords = chkP.get_plotting_coords()
		data.append(
			plygo.Scatter(
				x=coords[:,0],
				y=coords[:,1],
				mode = 'lines',
				line=dict(
					color="rgba(255,0,0,0.5)",
					width=4
				),
				hoverinfo='skip', #dont show datapoints on mouse over
				name='',
			)
		)
		if(sample_trajectories):
			if (len(chkP.heights)==0) :
				hovertext = ""
			else :
				hovertext = "Mean height: "+str(round((np.asarray(chkP.heights).mean()),2))+"m<br>Mean vel: "+str(round((np.linalg.norm(np.asarray(chkP.vels),axis=1).mean()),2))+"m/s"
			annotations.append(
				dict(
					x=coords[0,0],
					y=coords[0,1],
					yanchor='middle',
					xanchor='right',
					xref="x",
					yref="y",
					text=str(round(chkP.crossings_ratio*100,1))+"%",
					ax=0,
					ay=30,
					showarrow=True,
					textangle=-90,
					bordercolor="rgba(255,0,0,0.5)",
					arrowcolor="rgba(255,0,0,0.5)",
					borderwidth=2,
					arrowwidth=2,
					borderpad=1,
					bgcolor="rgba(255,255,255,1)",
					hovertext=hovertext
			)
		)
	
	#3- plot sample trajectories:
	if(sample_trajectories):
		rocks_data = plot_sample_trajectories(s,nb=sample_trajectories, use_plotly=True)
		for rock_data in rocks_data:
			color=s.random_generator.randint(255,size=3)
			color="rgb("+",".join(color.astype(str))+")"
			#parabolas:
			data.append(
				plygo.Scatter(
					x=rock_data[0],
					y=rock_data[1],
					mode = 'lines',
					line=dict(
						color=color,
						width=1
					),
					hoverinfo='skip', #dont show datapoints on mouse over
					name='',
				)
			)
			#trees:
			data.append(
				plygo.Scatter(
					x=rock_data[2],
					y=rock_data[3],
					mode = 'markers',
					marker = dict(
						symbol = 'triangle-up',
						size = 6,
						#line = dict(width=2),
						color = color,
						opacity = 1
					),
					hoverinfo='skip', #dont show datapoints on mouse over
					name='',
				)
			)
		cdf=s.get_stops_cdf()
		data+=[
			plygo.Scatter(
				x=[seg_points[0,0],seg_points[-1,0]],
				y=[bbox[2]]*2,
				fill='none',
				line=dict(
						color="rgba(255,255,255,0)",
						width=0
				),
				hoverinfo='skip',
			),
			plygo.Scatter(
				x=cdf[0,:],
				y=cdf[1,:]*(s.terrain.get_z_range()[1]-bbox[2])+bbox[2],
				fill='tonexty',
				text=["CDF = "+str(value) for value in cdf[1,:]],
				name="CDF",
				hoverinfo='text',
				mode = 'lines',
				line=dict(
					color="rgba(0,0,0,0.7)",
					width=2,
					shape='hv',
				),
				fillcolor="rgba(0,0,0,0.15)",
			)
		]
	
	#4- Configure layout (axes, etc...):
	xrange=bbox[:2]
	yrange=bbox[2:]
	layout = plygo.Layout(
		autosize=False,
		width=1000,
		height=800,
		margin=plygo.layout.Margin(
			l=40,
			r=10,
			b=20,
			t=30,
			pad=4
		),
		xaxis = dict(
			#nticks = 10,
			linecolor= 'black',
			mirror=True,
			showgrid=True,
			range = xrange,
			zeroline=False,
		),
		yaxis = dict(
			linecolor= 'black',
			mirror=True,
			showgrid=True,
			zeroline=False,
			scaleanchor = "x", #to make 1:1 scale
			range = yrange,
		),
		showlegend= False,
		hovermode = 'closest',
		annotations=annotations,
	)
	
	#5- configure plotly menubar:
	config = dict(
		modeBarButtonsToRemove = ["autoScale2d","hoverCompareCartesian","hoverClosestCartesian","select2d","lasso2d"],
		displaylogo = False,
		displayModeBar = True,
	)
	
	#6- Generate plotly html/js:
	ply_fig = plygo.Figure(data=data, layout=layout)
	return plyo.plot(ply_fig, config=config, show_link=False, output_type="div", include_plotlyjs=False)

def get_plotly_rock_raw_html(s,r):
	data = []
	
	def plot_rock():
		points=np.copy(r.vertices)
		if not s.random_rocks_ori:
			Math.rotate_points_around_origin(points,np.radians(s.rocks_ori))
		vertices = plygo.Mesh3d(
			x=points[:,0].tolist()*2,
			z=points[:,1].tolist()*2,
			y=[-r.ly/2]*len(points)+[r.ly/2]*len(points),
			alphahull=0,
			opacity=0.5,
			hoverinfo="x+y+z",
		)
		data.append(vertices)
		scatter_x=(points[:,0].tolist()+[points[0,0]]+[None])*2
		scatter_z=(points[:,1].tolist()+[points[0,1]]+[None])*2
		scatter_y=[-r.ly/2]*int((len(scatter_z)/2))+[r.ly/2]*int((len(scatter_z)/2))
		for p in points:
			scatter_x+=[p[0],p[0],None]
			scatter_z+=[p[1],p[1],None]
			scatter_y+=[-r.ly/2,r.ly/2,None]
		vertices = plygo.Scatter3d(
			x=scatter_x,
			y=scatter_y,
			z=scatter_z,
			mode='lines',
			name='',
			line=dict(color='black', width=5),
			hoverinfo='skip',
		)
		data.append(vertices)
	for v in [s.rocks_min_vol,s.rocks_max_vol]:
		r.set_volume(v)
		plot_rock()
		if (abs(s.rocks_max_vol-v)<1e-10): #don't plot a second rock if rocks_min_vol == rocks_max_vol.
			break
	data.append(
		plygo.Scatter3d(
			x=[0],
			y=[0],
			z=[0],
			text="COG",
			hoverinfo="text",
			marker = dict(
				symbol = 'circle',
				size = 5,
				color="black",
			),
		)
	)
	camera = dict(
		eye=dict(x=-1.55, y=-3.4, z=0.65),
		center=dict(x=0,y=0,z=0),
		projection_type="orthographic",
	)
	layout = plygo.Layout(
		width=380,
		height=380,
		margin=plygo.layout.Margin(
			l=1,
			r=1,
			b=1,
			t=1,
			pad=5
		),
		scene_camera=camera,
		scene_aspectmode='data',
		showlegend= False,
		hovermode = 'closest',
		scene = dict(
			xaxis=dict(
				showspikes=False
			),
			yaxis=dict(
				showspikes=False
			),
			zaxis=dict(
				showspikes=False
			)
		)
	)

	config = dict(
		displayModeBar= False,
		responsive= True,
	)
	
	ply_fig = plygo.Figure(data=data, layout=layout)
	return plyo.plot(ply_fig, config=config, show_link=False, output_type="div", include_plotlyjs=False)











