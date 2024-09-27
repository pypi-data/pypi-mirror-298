"""
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import vtk,time
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
import numpy as np
from threading import Thread
import platrock
import platrock.ThreeD.Objects as Objects
import platrock.Common.Math as Math

V=None
S=None #platrock simulation
ipythonshell=None

class SimRunThread(Thread):
	def run(self):
		# s=Simulations.current_simulation
		S.run()
class IpythonShellThread(Thread):
	def run(self):
		global ipythonshell
		from IPython.terminal.embed import InteractiveShellEmbed
		ipythonshell = InteractiveShellEmbed()
		ipythonshell()
	def exit(self):
		sys.exit()


def updateTO(TO):
	if TO.pos is not None:
		TO.VTK_actor.SetPosition(TO.pos)
		TO.VTK_actor.SetOrientation(0.,0.,0.)
		TO.VTK_actor.RotateWXYZ(TO.ori.angle()/np.pi*180.,TO.ori.vec[0],TO.ori.vec[1],TO.ori.vec[2])

		if hasattr(TO,'enable_points_view') and TO.enable_points_view :
			for p in TO.points:
				point_global_rf=p.pos
				p.VTK_actor.SetPosition(point_global_rf)
				p.VTK_actor.GetProperty().SetColor(p.color)
		if hasattr(TO,'bounding_box'):
			updateBoundingBox(TO)

def updateBoundingBox(TO):
	TO.bounding_box.VTK_actor.SetPosition(TO.bounding_box.pos)
	TO.bounding_box.vtk_source.SetXLength(TO.bounding_box.half_length*2)
	TO.bounding_box.vtk_source.SetYLength(TO.bounding_box.half_length*2)
	TO.bounding_box.vtk_source.SetZLength(TO.bounding_box.half_length*2)

def updateTerrainTO(TO):
	for f in TO.faces:
		f.VTK_actor.GetProperty().SetColor(f.color)
	#V.iren.Render()

def updateTreesColor(terrain):
	for tree in terrain.trees:
		tree.VTK_actor.GetProperty().SetColor(tree.color)
	#V.iren.Render()

def updateTerrainColors(TO):
	colors=vtk.vtkUnsignedCharArray()
	colors.SetNumberOfComponents(3)
	faces_colors=(np.asarray([f.color for f in TO.faces])*255).astype(int)
	for fc in faces_colors:
		colors.InsertNextTuple3(fc[0],fc[1],fc[2])
	TO.vtk_polydata.GetCellData().SetScalars(colors)

def draw_rock(r):
	if(type(r)==Objects.Sphere):
		V.addSphere(r)
	else:
		V.addTriangulatedSurface(r)
	if hasattr(r,'enable_points_view') and r.enable_points_view:
		V.addPointsSpheres(r)
	if hasattr(r, 'bounding_box'):
		V.addBoundingBox(r)
	V.iren.Render()

def draw_trees():
	V.addTrees(S.terrain)
	V.ren.ResetCamera()
	V.iren.Render()

def take_snapshot(filename):
	windowto_image_filter = vtk.vtkWindowToImageFilter()
	windowto_image_filter.SetInput(V.ren_win)
	windowto_image_filter.SetMagnification(1)  # image quality
	windowto_image_filter.SetInputBufferTypeToRGB()
	# Read from the front buffer.
	windowto_image_filter.ReadFrontBufferOff()
	windowto_image_filter.Update()
	
	writer = vtk.vtkPNGWriter()
	writer.SetFileName(filename)
	writer.SetInputConnection(windowto_image_filter.GetOutputPort())
	writer.Write()


class Window3D(object):
	def setup(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1000, 700)
		self.centralWidget = QtWidgets.QWidget(MainWindow)
		self.gridlayout = QtWidgets.QGridLayout(self.centralWidget)
		self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
		self.gridlayout.addWidget(self.vtkWidget, 0, 0, 1, 1)
		self.start_stop_button = QtWidgets.QPushButton("START")
		
		self.start_stop_button.clicked.connect(self.handle_start_stop_button)
		self.gridlayout.addWidget(self.start_stop_button,0,1,1,2)

		MainWindow.setCentralWidget(self.centralWidget)
		
		self.timer = QtCore.QTimer()
		self.timer.setInterval(int(1000/30)) #1000/fps
		self.timer.timeout.connect(self.refresh)
		self.timer.start()
		
		self.forestInitialDrawDone = False
	
	def refresh(self):
		# s=Simulations.current_simulation
		if V is not None and S.current_rock is not None:
			if S.current_rock.VTK_actor is None :
				draw_rock(S.current_rock)
			if S.enable_forest and not self.forestInitialDrawDone:
				draw_trees()
				self.forestInitialDrawDone=True
			updateTO(S.current_rock)
			updateTerrainColors(S.terrain)
			updateTreesColor(S.terrain)
			if S.current_rock.pos is not None:
				V.camera.SetFocalPoint(S.current_rock.pos)
			V.iren.Render()
	
	def handle_start_stop_button(self):
		if(not S.status=="running"):
			S.status="running"
		else:
			S.status="pause"


class View3D(QtWidgets.QMainWindow):
	def __init__(self, parent = None,):
		QtWidgets.QMainWindow.__init__(self, parent)
		self.window = Window3D()
		self.window.setup(self)
		# VTK renderer :
		self.ren = vtk.vtkRenderer()
		self.ren.SetBackground(0.2,0.2,0.2)
		self.ren_win = self.window.vtkWidget.GetRenderWindow()
		self.ren_win.AddRenderer(self.ren)
		self.iren = self.ren_win.GetInteractor()
		self.iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
		#self.iren.GetInteractorStyle().SetInteractionModeToImage3D()
		self.addAxes()
		self.camera=self.ren_win.GetRenderers().GetFirstRenderer().GetActiveCamera()
		self.time_last_updated=0
		
	def addAxes(self):
		transform = vtk.vtkTransform()
		terrain_points=S.terrain.points_as_array
		transform.Translate(0.0, 0.0, terrain_points[:,2].mean())
		axes = vtk.vtkAxesActor()
		#  The axes are positioned with a user transform
		axes.SetUserTransform(transform)
		self.ren.AddActor(axes)
	
	def addTriangulatedSurface(self,TO):
		# here the entire "TO" has one actor
		points = vtk.vtkPoints()
		triangles = vtk.vtkCellArray()
		
		for i,p in enumerate(TO.points):
			p._temp_id=i
			points.InsertPoint(i,p.relPos[0],p.relPos[1],p.relPos[2])
		for f in TO.faces:
			triangle = vtk.vtkTriangle()
			triangle.GetPointIds().SetId(0,f.points[0]._temp_id)
			triangle.GetPointIds().SetId(1,f.points[1]._temp_id)
			triangle.GetPointIds().SetId(2,f.points[2]._temp_id)
			triangles.InsertNextCell(triangle)
			f.vtk_source=triangle
			i+=1
			
		# polydata object
		pd = vtk.vtkPolyData()
		pd.SetPoints( points )
		pd.SetPolys( triangles )
		TO.vtk_polydata=pd
		# mapper
		mapper = vtk.vtkPolyDataMapper()
		if vtk.VTK_MAJOR_VERSION <= 5:
			mapper.SetInput(pd)
		else:
			mapper.SetInputData(pd)
			
		# actor
		actor = vtk.vtkActor()
		actor.SetMapper(mapper)
		actor.GetProperty().SetColor(TO.color)
		actor.GetProperty().SetOpacity(1)
		actor.GetProperty().SetEdgeVisibility(True)
		self.ren.AddActor(actor)
		TO.VTK_actor=actor
	
	def addTrees(self,terrain):
		lowest_terrain_point_z=terrain.points_as_array[:,2].min()
		highest_terrain_point_z=terrain.points_as_array[:,2].max()+50.
		cylinders_height=highest_terrain_point_z-lowest_terrain_point_z
		
		for t in terrain.trees:
			source = vtk.vtkCylinderSource()
			source.SetCenter(0,0,0)
			source.SetResolution(10)
			source.SetRadius(t.dhp/2./100)
			source.SetHeight(cylinders_height)
			
			mapper = vtk.vtkPolyDataMapper()
			if vtk.VTK_MAJOR_VERSION <= 5:
				mapper.SetInput(source.GetOutput())
			else:
				mapper.SetInputConnection(source.GetOutputPort())
			
			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetColor(t.color)
			actor.RotateX(90.0)
			actor.SetPosition([t.pos[0],t.pos[1],lowest_terrain_point_z+cylinders_height/2.])
			self.ren.AddActor(actor)
			t.VTK_actor=actor
	
	def addSphere(self,sph_obj):
		source = vtk.vtkSphereSource()
		source.SetCenter(0,0,0)
		source.SetRadius(sph_obj.radius)
		
		# mapper
		mapper = vtk.vtkPolyDataMapper()
		if vtk.VTK_MAJOR_VERSION <= 5:
			mapper.SetInput(source.GetOutput())
		else:
			mapper.SetInputConnection(source.GetOutputPort())

		# actor
		actor = vtk.vtkActor()
		actor.SetMapper(mapper)
		actor.GetProperty().SetColor(sph_obj.color)
		actor.GetProperty().SetOpacity(sph_obj.opacity)
		actor.SetPosition(sph_obj.pos)
		# assign actor to the renderer
		self.ren.AddActor(actor)
		sph_obj.VTK_actor=actor	
	
	def addPointsSpheres(self,TO):
		for p in TO.points:
			source = vtk.vtkSphereSource()
			source.SetCenter(0,0,0)
			source.SetRadius(p.radius)
			
			# mapper
			mapper = vtk.vtkPolyDataMapper()
			if vtk.VTK_MAJOR_VERSION <= 5:
				mapper.SetInput(source.GetOutput())
			else:
				mapper.SetInputConnection(source.GetOutputPort())
	
			# actor
			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetColor(p.color)
			actor.GetProperty().SetOpacity(TO.opacity)
			point_global_rf=p.pos
			actor.SetPosition(point_global_rf)
			# assign actor to the renderer
			self.ren.AddActor(actor)
			p.VTK_actor=actor
			if(len(TO.points)==1):	#spheres for instance
				TO.VTK_actor=actor
	
	def addBoundingBox(self,TO):
		source = vtk.vtkCubeSource()
		source.SetCenter(0,0,0)
		source.SetXLength(TO.bounding_box.half_length*2)
		source.SetYLength(TO.bounding_box.half_length*2)
		source.SetZLength(TO.bounding_box.half_length*2)
		#source.SetThetaResolution(50)
		#source.SetPhiResolution(50)
		TO.bounding_box.vtk_source=source
		mapper = vtk.vtkPolyDataMapper()
		if vtk.VTK_MAJOR_VERSION <= 5:
			mapper.SetInput(source.GetOutput())
		else:
			mapper.SetInputConnection(source.GetOutputPort())
		actor = vtk.vtkActor()
		actor.SetMapper(mapper)
		actor.GetProperty().SetColor(0.53,0.8,0.92)
		actor.GetProperty().SetOpacity(TO.bounding_box.opacity)
		actor.SetPosition(TO.bounding_box.pos)
		# assign actor to the renderer
		self.ren.AddActor(actor)
		TO.bounding_box.VTK_actor=actor
	
	def addAngVel(self,rock):
		if(rock.angVel.norm()>0):
			
			
			cylinder_length=rock.angVel.norm()
			x,y,z=rock.angVel.normalized()*cylinder_length
			rotation=Math.Vector3([0,1,0]).cross(rock.angVel)
			angle=np.arcsin(y / np.sqrt(sum(rock.angVel**2)))
			source = vtk.vtkCylinderSource()
			#source.SetCenter(0,0,0)
			source.SetResolution(10)
			source.SetRadius(rock.radius/5.)
			source.SetHeight(np.sqrt(x**2 + y**2 + z**2))
			transform = vtk.vtkTransform()
			transform.Translate(rock.pos+0.5*Math.Vector3([x,y,z]))
			transform.RotateWXYZ(np.degrees(angle),rotation_axis[0],rotation_axis[1],rotation_axis[2])
			
			transformFilter=vtk.vtkTransformPolyDataFilter()
			transformFilter.SetTransform(transform)
			transformFilter.SetInputConnection(source.GetOutputPort())
			transformFilter.Update()
			
			mapper = vtk.vtkPolyDataMapper()
			mapper = vtk.vtkPolyDataMapper()
			if vtk.VTK_MAJOR_VERSION <= 5:
				mapper.SetInput(transformFilter.GetOutput())
			else:
				mapper.SetInputConnection(transformFilter.GetOutputPort())
			
			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			#actor.GetProperty().SetColor(t.color)
			#actor.RotateWXYZ(angle,np.degrees(rotation_axis[0]),np.degrees(rotation_axis[1]),np.degrees(rotation_axis[2]))
			#actor.SetPosition()
			self.ren.AddActor(actor)
			#rock.VTK_angVel_actor=actor

def initialize(sim):
	global V, S
	S=sim
	app = QApplication(sys.argv)
	view = View3D()
	view.show()
	view.iren.Initialize() # Need this line to actually show the render inside Qt
	V=view #FIXME : should be useless later
	# s=Simulations.current_simulation
	S.GUI=View3D
	if(S.terrain):draw_rock(S.terrain)
	V.ren.ResetCamera()

	def launchapp():
		app.exec_()
		ipythonShellThread.exit()
		ipythonShellThread.join()
		time.sleep(1)

	simRunThread=SimRunThread()
	simRunThread.setDaemon(True)
	simRunThread.start()

	ipythonShellThread=IpythonShellThread()
	ipythonShellThread.setDaemon(True)
	ipythonShellThread.start()

	sys.exit(launchapp())




