# Vision_1 macro
# --------------------
#
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as 
# published by the Free Software Foundation, either version 3 of the 
# License, or (at your option) any later version.
#  
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#  
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# --------------------
__Title__="Vision_5"
__Author__ = "freedman, Chris Berg"
__Version__ = "5.55"
__Date__    = "2020-08-27"
__Comment__ = ""
__Web__ = "https://forum.freecadweb.org/viewtopic.php?f=22&t=33413"
__Wiki__ = "http://www.freecadweb.org/wiki/index.php?title=Vision_5"
__Icon__  = "/usr/lib/freecad/Mod/plugins/icons/Vision_5"
__Status__ = "New"
__Requires__ = "freecad 0.18"
__Communication__ = "http://www.freecadweb.org/wiki/index.php?title=User:freedman" 

import FreeCAD
from PySide import QtGui,QtCore
import FreeCAD as App
import FreeCADGui as gui


class CB_ToolBox(QtGui.QDockWidget):
    def __init__(self):
        super(CB_ToolBox, self).__init__()
        self.setParent(Gui.getMainWindow())
        self.setObjectName("Vis5-V55")
        self.setWindowTitle("V5")
        self.initGui()
        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint ) 
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setAutoFillBackground(True)
        self.tree_select = False
        self.set_sketch_at_5 = False
        self.go_3D = False
        self.current_tansparency = 0
        self.nav_flag = False
        self.view_back = False
        self.hide_flag =False
        self.show_flag =False
        self.swap_view = True
        self.on_set_100 =False
        self.on_set_50 =False
        self.on_set_10 =False
        self.on_shade_lines = False
        self.shade_line_toggle = True
        self.object_part_flag =True
        self.page_number =1.01
        self.part_lock =True
        self.part_lock_toggle =True
    
        self.show_object = False
        self.pic_vis_at = False 
        self.pic_vis_at_value = 90
        self.mode_wireframe= False
        self.in_sketcher = False
        self.a = 2.0     #color
        self.b = 4.0
        self.c = 20.0  
        self.dmode_text =  "Shaded"      
       
        p=App.ParamGet("User parameter:BaseApp/Preferences/View")         # store navigation style
        self.q_style=p.GetString("NavigationStyle")

        Gui.runCommand('Std_DrawStyle',0)            # set draw style
        Gui.Selection.clearSelection()

        self.page_number = 1.02
        self.vis_mod(0,0)
        self.vis_mod(1,0)
        self.round_for_display(False) 
  

      
      
    def initGui(self):    #   0         1       2        
                            # handle, text, position, height, 
        self.close_list =[["button0",  "Exit Macro" ,0  ]]
       
        self.sketch_list =[["button0",  " 2D / Back" ,0  ],
                             ["button1",  "Inventor"  ,0 ],
                            ["button2",  "Close " ,0  ]]

        self.global_list =[["button0",  "Vis=100" ,0  ], 
                            ["button1",  "Vis=50 " ,0  ], 
                            ["button2",  "Vis=5 " ,0  ],
                            ["button3",  "Shade/Line" ,0  ]] 

        self.singles_list =[["button0",  " Vis=100 " ,0],
                            ["button1",  " Vis=50"  ,0 ],
                            ["button2",  " Vis=10"  ,0 ]]
                            
        self.editor_list =[["button0",  " Set Mask"  ,2 ],
                           ["button1",  "Suppress "  ,0 ],
                           ["button2",  " Object"  ,0 ],
                           ["button3",  " Next"  ,0 ],
                           ["button4",  " Prev"  ,0 ],
                           ["button5",  "Reset All" ,0 ]] 

        self.res_list =[["button0",  "High"  ,0 ],  
                            ["button1",  " Med " ,0  ], 
                            ["button2",  "Low"  ,0 ]]
        
        self.acc_list =[["button0",  "Focus Tree"  ,0 ],    
                            ["button1",  "3D View\n Sketch" ,1 ],
                            ["button2",  "Color All" ,0 ]]

                         
        self.wid = QtGui.QWidget()
        self.lay = QtGui.QVBoxLayout()
        self.lay.setContentsMargins(0,0,0,0)
        self.setGeometry(1100, 120, 58, 60)      # define window		xLoc,yLoc,xDim,yDim
 ##       self.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea )
        self.setMaximumSize(58,630)
   
    
        for i in range(len(self.close_list)):      
            self.build_button(i,self.close_list)
        self.L1=QtGui.QLabel("  Sketch ", self) ;  self.L1.setFixedWidth(55) ;  self.L1.setMaximumHeight(14)  ;  color="background-color:wheat;" ;   font="font-weight:bold;" ;  self.L1.setStyleSheet(color + font ) ; self.lay.addWidget(self.L1,0)
        for i in range(len(self.sketch_list)):        # init options
            self.build_button(i,self.sketch_list)
        self.L1=QtGui.QLabel("   Global ", self) ;  self.L1.setFixedWidth(55) ;   self.L1.setMaximumHeight(14)  ;color="background-color:wheat;" ;   font="font-weight:bold;" ;  self.L1.setStyleSheet(color + font ) ; self.lay.addWidget(self.L1,0)
        for i in range(len(self.global_list)):        # init options
            self.build_button(i,self.global_list)
        self.L1=QtGui.QLabel("   Single ", self) ;  self.L1.setFixedWidth(55) ;   self.L1.setMaximumHeight(14)  ;color="background-color:wheat;" ;   font="font-weight:bold;" ;  self.L1.setStyleSheet(color + font ) ; self.lay.addWidget(self.L1,0)
        for i in range(len(self.singles_list)):        # init options
            self.build_button(i,self.singles_list)
        self.L1=QtGui.QLabel(" Page Edit", self) ;  self.L1.setFixedWidth(55) ;   self.L1.setMaximumHeight(14)  ;color="background-color:wheat;" ;   font="font-weight:bold;" ;  self.L1.setStyleSheet(color + font ) ; self.lay.addWidget(self.L1,0)
        for i in range(len(self.editor_list)):         # init options
            self.build_button(i,self.editor_list)    
        self.L1=QtGui.QLabel(" View RES", self) ;  self.L1.setFixedWidth(55) ;   self.L1.setMaximumHeight(14)  ;color="background-color:wheat;" ;   font="font-weight:bold;" ;  self.L1.setStyleSheet(color + font ) ; self.lay.addWidget(self.L1,0)
        for i in range(len(self.res_list)):        # init options
            self.build_button(i,self.res_list)
        self.L1=QtGui.QLabel("    Extra ", self) ;  self.L1.setFixedWidth(55) ;   self.L1.setMaximumHeight(14)  ;color="background-color:wheat;" ;   font="font-weight:bold;" ;  self.L1.setStyleSheet(color + font ) ; self.lay.addWidget(self.L1,0)
        for i in range(len(self.acc_list)):        # init options
            self.build_button(i,self.acc_list)

     

############    connects               #####################################################################################
        self.close_list[0][0].clicked.connect(self.on_close_app)
       
        self.sketch_list[0][0].clicked.connect(self.on_reset_2D) 
        self.sketch_list[1][0].clicked.connect(self.on_sketch_inventor)
        self.sketch_list[2][0].clicked.connect(self.on_close_sketch)      

        self.global_list[0][0].clicked.connect(self.on_vis_100)
        self.global_list[1][0].clicked.connect(self.on_vis_50)
        self.global_list[2][0].clicked.connect(self.on_vis_5)
        self.global_list[3][0].clicked.connect(self.on_shade_or_lines_global)

        self.singles_list[0][0].clicked.connect(self.on_vis_pick_100)
        self.singles_list[1][0].clicked.connect(self.on_vis_pick_50)
        self.singles_list[2][0].clicked.connect(self.on_vis_pick_10)
        

        self.editor_list[0][0].clicked.connect(self.on_show_hide)
        self.editor_list[1][0].clicked.connect(self.on_wireframe_solid)
        self.editor_list[2][0].clicked.connect(self.on_object_part) 
        self.editor_list[3][0].clicked.connect(self.on_next) 
        self.editor_list[4][0].clicked.connect(self.on_prev)
        self.editor_list[5][0].clicked.connect(self.view_all) 

 
        self.res_list[0][0].clicked.connect(self.on_high_res)
        self.res_list[1][0].clicked.connect(self.on_med_res)
        self.res_list[2][0].clicked.connect(self.on_low_res)

        self.acc_list[0][0].clicked.connect(self.on_tree_select)
        self.acc_list[1][0].clicked.connect(self.on_3D_select)
        self.acc_list[2][0].clicked.connect(self.on_color_all)
        

        for chi in self.wid.children():      #   align buttons
            self.lay.setAlignment(chi, QtCore.Qt.AlignHCenter)
        self.wid.setLayout(self.lay)
        self.setWidget(self.wid)
        self.show()   # set buttons on the RIGHT

        mw=Gui.getMainWindow()
        mw.workbenchActivated.connect(self.wbChange)

        self.disable_sketch_buttons()
 
        self.editor_list[5][0].setEnabled(False) 
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_stopped) 
        


################    control to detect WB  ###########################################

    def wbChange(self,name):
        active = Gui.activeWorkbench().__class__.__name__
        if active == "SketcherWorkbench":
            self.current_view = Gui.ActiveDocument.ActiveView.getCamera()
            self.in_sketcher = True
            self.disable_pick_showhide()
            self.set_background_yellow()
            self.enable_sketch_buttons()
            self.timer.start(0)         # this will run timer_stopped

        if active != "SketcherWorkbench":
            p=App.ParamGet("User parameter:BaseApp/Preferences/View")
            p.SetString("NavigationStyle", str(self.q_style))
            self.in_sketcher = False 
            self.disable_sketch_buttons()
            self.set_background_khaki()
            self.enable_pick_showhide() 
            self.disable_sketch_buttons()
            self.nav_flag = False
 
            
    def timer_stopped(self):
        self.timer.stop()
        self.vis_mod(1,0)  # exit vision editor
        if self.go_3D== True:
            self.view_back = False
            self.on_reset_2D()
        else:
            self.view_back = False
        if self.tree_select==True:
            self.set_combo_tree()  # show the tree instead of Task

    def test_doc_4_no_tip(self):        # currently this looks for Tip errors
        doc = FreeCAD.ActiveDocument
        for obj in doc.Objects:
            if hasattr(obj.ViewObject,'PointSize')  and str(obj.TypeId) != "Sketcher::SketchObject": #  and str(type(obj)) != "<class 'PrimitivePy'>":
                if str(obj.TypeId) != "PartDesign::Plane" and str(obj.TypeId) != "App::Origin" and str(obj.TypeId) != "App::Plane" and str(obj.TypeId) != "App::Line"  and str(obj.TypeId) != "PartDesign::ShapeBinder" and str(obj.Name) != "ShapeString":  
                    if str(obj) == "<body object>" or  str(obj) == "<PartDesign::FeatureBase>" or str(obj) == '<Part::PartFeature>':
                        if hasattr(obj,'Tip'):
                            if obj.Tip is None:
                                print ("No Tip in object identified",obj.Name)



###################   connections  to buttons   ##############################################################################

    def on_reset_2D(self):          
        if self.view_back == True:
            self.current_view = Gui.ActiveDocument.ActiveView.getCamera()  
            Gui.ActiveDocument.ActiveView.setCameraOrientation(App.Placement(Gui.editDocument().EditingTransform).Rotation.Q)       # set to 2D view
            self.view_back = False
        else:
            self.view_back = True 
            Gui.ActiveDocument.ActiveView.setCamera(self.current_view)    

    def on_sketch_inventor(self):
        if self.nav_flag == False:
            p=App.ParamGet("User parameter:BaseApp/Preferences/View")
            self.q_style=p.GetString("NavigationStyle")
            p.SetString("NavigationStyle","Gui::InventorNavigationStyle")
            self.nav_flag = True
            color="background-color:yellow;" ;  
            self.sketch_list[1][0].setStyleSheet(color)
            self.set_background_darkorange()
        else: 
            p=App.ParamGet("User parameter:BaseApp/Preferences/View")
            p.SetString("NavigationStyle", str(self.q_style)) 
            self.nav_flag = False
            color="background-color:lightcyan;" 
            self.sketch_list[1][0].setStyleSheet(color)
            self.set_background_yellow()   

    def on_close_sketch(self):
        p=App.ParamGet("User parameter:BaseApp/Preferences/View")
        p.SetString("NavigationStyle", str(self.q_style)) 
        Gui.ActiveDocument.resetEdit()
        App.ActiveDocument.recompute()
        App.ActiveDocument.commitTransaction()
        if self.tree_select==True:
            self.set_combo_tree()
        self.disable_sketch_buttons()
        self.stored_view = Gui.ActiveDocument.ActiveView.getCamera() 
        self.editor_list[4][0].setEnabled(True) ;  self.editor_list[5][0].setEnabled(True)


    def on_view_show(self):
        self.current_view = Gui.ActiveDocument.ActiveView.getCamera()
        Gui.ActiveDocument.ActiveView.setCamera(self.stored_view)
               
    def on_high_res(self):
        doc = FreeCAD.ActiveDocument
        for obj in doc.Objects:
            if obj.TypeId[:4] == 'Part' or obj.TypeId == "Sketcher::SketchObject":
                if hasattr(obj.ViewObject,'Deviation'):  # should be a sketch
                    obj.ViewObject.Deviation = 0.05 ;        obj.ViewObject.AngularDeflection = 10.0

    def on_med_res(self):
        doc = FreeCAD.ActiveDocument
        for obj in doc.Objects:
            if obj.TypeId[:4] == 'Part' or obj.TypeId == "Sketcher::SketchObject":
                if hasattr(obj.ViewObject,'Deviation'):  # should be a sketch
                    obj.ViewObject.Deviation = 0.1 ;        obj.ViewObject.AngularDeflection = 28.5

    def on_low_res(self):
        doc = FreeCAD.ActiveDocument
        for obj in doc.Objects:
            if obj.TypeId[:4] == 'Part' or obj.TypeId == "Sketcher::SketchObject":
                if hasattr(obj.ViewObject,'Deviation'):  # should be a sketch
                   obj.ViewObject.Deviation = 0.2 ;        obj.ViewObject.AngularDeflection = 28.5

#########################################
    def on_vis_100(self): 
        self.set_transparency_all(0)	#  self.set_opt_button_color(3,opt_vis,1) 
        self.current_transparency=0 
        Gui.Selection.clearSelection()   
    
    def on_vis_50(self): 
        self.set_transparency_all(50)	#  self.set_opt_button_color(3,opt_vis,1) 
        self.current_transparency=50 
        Gui.Selection.clearSelection()      
 
    def on_vis_5(self): 
        self.set_transparency_all(95)	#  self.set_opt_button_color(3,opt_vis,1)  
        self.current_transparency=95
        Gui.Selection.clearSelection()  

    def on_shade_or_lines_global (self):
        if self.shade_line_toggle == True:
            self.shade_line_toggle = False
            self.global_list[3][0].setText("Flat Lines")
        else:
            self.shade_line_toggle = True
            self.global_list[3][0].setText("Shaded")
        doc = FreeCAD.ActiveDocument
        for obj in doc.Objects:
            if hasattr(obj.ViewObject,'PointSize')  and str(obj.TypeId) != "Sketcher::SketchObject": #  and str(type(obj)) != "<class 'PrimitivePy'>":
                if str(obj.TypeId) != "PartDesign::Plane" and str(obj.TypeId) != "App::Origin" and str(obj.TypeId) != "App::Plane" and str(obj.TypeId) != "App::Line"  and str(obj.TypeId) != "PartDesign::ShapeBinder" and str(obj.Name) != "ShapeString":  
                    if str(obj) == "<body object>" or  str(obj) == "<PartDesign::FeatureBase>" or str(obj) == '<Part::PartFeature>':
                        if str(obj.TypeId) != "Part::Helix" and str(obj.TypeId) != "Part::Spiral" and str(obj.TypeId) != "Part::Line" and str(obj.TypeId) != "Part::Ellipse" and str(obj.Name) != "BaseFeature":
                            if str(obj.TypeId) != "Part::RegularPolygon" and str(obj.TypeId) != "Part::Circle" :
                                #FreeCAD.Console.PrintMessage("obj.Name = "+obj.Name+"\nobj.Label = "+obj.Label+"\nstr(obj) = "+str(obj)+"\nstr(type(obj)) = "+str(type(obj))+ "\nobj.TypeId = "+obj.TypeId  +  " \n\n")
                                if self.shade_line_toggle == True:                            
                                    obj.ViewObject.DisplayMode  = u"Shaded"
                                    self.dmode_text = u"Shaded" 
                                else:                            
                                    obj.ViewObject.DisplayMode  =  u"Flat Lines" 
                                    self.dmode_text = u"Flat Lines"
                       
                        
########$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def on_vis_pick_100(self):
        if self.on_set_100 == False:
            Gui.Selection.clearSelection()
            self.pic_vis_at = True ; self.pic_vis_at_value = 0 ; self.on_set_10 = False ; self.on_set_50 = False ; self.on_set_100 = True ; color="background-color:palegreen;" ;  self.singles_list[0][0].setStyleSheet(color)
            color="background-color:lightcyan;" ;  self.singles_list[1][0].setStyleSheet(color) ; self.singles_list[2][0].setStyleSheet(color)
            self.show_flag = False ; self.show_object =False
            color="background-color:lightcyan;" ;  self.editor_list[0][0].setStyleSheet(color) ; self.editor_list[1][0].setStyleSheet(color) ; self.set_background_blue()
        else:
            self.clear_pick_buttons()
   
    def on_vis_pick_50(self):
        if self.on_set_50 == False:
            Gui.Selection.clearSelection()
            self.pic_vis_at = True ; self.pic_vis_at_value = 50 ;  self.on_set_10 = False ; self.on_set_50 = True ; self.on_set_100 = False ; color="background-color:palegreen;" ;  self.singles_list[1][0].setStyleSheet(color)
            color="background-color:lightcyan;" ;  self.singles_list[0][0].setStyleSheet(color) ; self.singles_list[2][0].setStyleSheet(color)
            self.show_flag = False ; self.show_object =False
            color="background-color:lightcyan;" ;  self.editor_list[0][0].setStyleSheet(color) ; self.editor_list[1][0].setStyleSheet(color) ; self.set_background_blue()
        else:
            self.clear_pick_buttons()
     

    def on_vis_pick_10(self):
        if self.on_set_10 == False:
            Gui.Selection.clearSelection()
            self.pic_vis_at = True ; self.pic_vis_at_value = 90 ;  self.on_set_10 = True ; self.on_set_50 = False ; self.on_set_100 = False ;color="background-color:palegreen;" ;  self.singles_list[2][0].setStyleSheet(color)
            color="background-color:lightcyan;" ;  self.singles_list[0][0].setStyleSheet(color) ; self.singles_list[1][0].setStyleSheet(color)
            self.show_flag = False ; self.show_object =False
            color="background-color:lightcyan;" ;  self.editor_list[0][0].setStyleSheet(color) ; self.editor_list[1][0].setStyleSheet(color) ; self.set_background_blue()
        else:
            self.clear_pick_buttons()


    def set_transparency_all(self,data):
        doc = FreeCAD.ActiveDocument
        for obj in doc.Objects:
            if obj.TypeId[:4] == 'Part':
                if hasattr(obj,'ViewObject') and str(obj.TypeId) != "PartDesign::Plane"  and str(obj.TypeId) != "PartDesign::ShapeBinder" and str(obj.TypeId) != "Sketcher::SketchObject" and str(obj.TypeId) != "App::Plane" and str(obj.TypeId) != "App::Line":
                    if str(obj.TypeId) !='DisplayModeBody':
                        obj.ViewObject.Transparency=data

	    
    def on_wireframe_solid(self):
        if self.mode_wireframe ==False:
            self.editor_list[1][0].setText("Wireframe")
            self.mode_wireframe = True
        else:
            self.editor_list[1][0].setText("Suppress")
            self.mode_wireframe = False 

                       
#######################################################

    def set_combo_tree(self):
        mw = FreeCADGui.getMainWindow()
        dw= mw.findChildren(QtGui.QDockWidget)
        for i in dw:
            if i.objectName() == "Combo View":
                tab = i.findChild(QtGui.QTabWidget)
                tab.setCurrentIndex(0)

    def on_close_app(self):
        if  self.show_object ==  True:   # if exiting app then close the edit panel
            self.on_show_hide()   
        FreeCADGui.Selection.removeObserver(s) 
        p=App.ParamGet("User parameter:BaseApp/Preferences/View")
        p.SetString("NavigationStyle", str(self.q_style))
        self.close()

    def on_tree_select(self):
        if  self.tree_select ==False:
            self.tree_select =True ;  color="background-color:gold;" ;  self.acc_list[0][0].setStyleSheet(color)
        else:
            self.tree_select =False ;  color="background-color:lightcyan;" ;  self.acc_list[0][0].setStyleSheet(color)            

    def on_3D_select(self):
        if self.go_3D  == False:
            self.go_3D=True ;  color="background-color:gold;" ;  self.acc_list[1][0].setStyleSheet(color)
        else:        
            self.go_3D=False ;  color="background-color:lightcyan;" ;  self.acc_list[1][0].setStyleSheet(color)   

################################## ########################

    def clear_pick_buttons(self):
        self.pic_vis_at = False ; color="background-color:lightcyan;" ; self.singles_list[0][0].setStyleSheet(color) ; self.singles_list[1][0].setStyleSheet(color) ; self.singles_list[2][0].setStyleSheet(color)
        self.show_object =False ;  color="background-color:lightcyan;"  ;  self.editor_list[0][0].setStyleSheet(color)  
        self.editor_list[1][0].setStyleSheet(color); self.editor_list[2][0].setStyleSheet(color) ; self.editor_list[3][0].setStyleSheet(color); self.editor_list[4][0].setStyleSheet(color) ; self.editor_list[5][0].setStyleSheet(color)  
        self.set_background_lightcyan() ; 
        self.on_set_10 = False ; self.on_set_50 = False ; self.on_set_100 = False ; self.show_flag = False

    def set_background_khaki(self):
        if self.pic_vis_at == True or self.show_object == True:
            self.color="background-color:salmon;" 
        else:
            self.color="background-color::khaki;" ;  self.setStyleSheet(self.color)  ;  self.setAutoFillBackground(True)

    def set_background_blue(self):
        self.color="background-color:lightblue;" ;  self.setStyleSheet(self.color) ;  self.setAutoFillBackground(True) #salmon
 
    def set_background_darkorange(self):
        self.color="background-color:darkorange;" ; self.setStyleSheet(self.color) ;   self.setAutoFillBackground(True)

    def set_background_yellow(self):
        self.color="background-color:yellow;"  ;  self.setStyleSheet(self.color)  ;   self.setAutoFillBackground(True) 

    def set_background_lightcyan(self):
        self.color="background-color::lightcyan;"  ; self.setStyleSheet(self.color) ;   self.setAutoFillBackground(True)

    def round_for_display(self,state):
        self.page_quick=round( self.page_number   )
        self.page_quick = round( self.page_number - self.page_quick -.01,2)
        self.page_quick *= 100
        self.unsigned = int(self.page_quick)
        self.f_string = str(self.unsigned)
        if self.page_number == 1.01:
            self.text_string= "View all"
        else:
            if state==True:
                self.text_string= "Editing #"+ self.f_string
            else:
                self.text_string= " View #"+ self.f_string    
        self.editor_list[0][0].setText(self.text_string)
       

    def reset_display(self):
        self.page_quick=round( self.page_number  )
        self.page_quick = round( self.page_number - self.page_quick- .01,2)
        self.page_quick *= 100
        self.unsigned = int(self.page_quick)
        self.f_string = str(self.unsigned)
        if self.page_number == 1.01:
            self.text_string= "View all"
        else:
            self.text_string= "Reset#"+ self.f_string  + "+"
        self.editor_list[5][0].setText(self.text_string)


    def on_next(self):
         if self.show_flag == True and self.page_number <1.19:
            self.vis_mod(1,0)  # exit
            self.page_number =  round(self.page_number +.01,2)
            self.round_for_display(True)
            self.vis_mod(0,0)  # enter
            self.reset_display()

         elif self.show_flag == False:   # this is out of editing
            if self.page_number <1.19:
                if self.page_number ==1.01:
                    self.page_number = 1.02                    
                    self.vis_mod(0,0)  # enter
                    self.vis_mod(1,0)  # exit
                else:
                    self.page_number =  round(self.page_number +.01,2)
                    self.vis_mod(0,0)  # enter
                    self.vis_mod(1,0)  # exit
                self.round_for_display(False)
                self.reset_display()
      
    def on_prev(self):
        if self.show_flag == True and self.page_number > 1.02:
            self.vis_mod(1,0)
            self.page_number = round(self.page_number -.01,2)
            self.round_for_display(True)
            self.vis_mod(0,0)
            self.reset_display()
        else:                                    # this is out of editing
            if self.show_flag == False: 
                if self.page_number >1.02:
                    self.page_number =  round(self.page_number -.01,2)
                    self.round_for_display(False)
                    self.vis_mod(0,0)  # enter
                    self.vis_mod(1,0)  # exit
                    self.reset_display()
                elif self.page_number == 1.02:
                    self.page_number =  round(self.page_number -.01,2)
                    self.vis_mod(0,0)  # enter
                    self.vis_mod(1,0)  # exit
                    self.vis_mod(1,1)  # exit
                    self.round_for_display(False)
                    self.reset_display()          

    def on_object_part(self):
        if self.object_part_flag  == False:
            self.object_part_flag =True
            self.editor_list[2][0].setText(" Object")
            self.part_lock = True
            self.part_lock_toggle = True
        else:
            self.object_part_flag = False
            self.editor_list[2][0].setText(" Part")
            self.part_lock = False
            self.part_lock_toggle = False

    def view_all(self):
        Gui.Selection.clearSelection()
        self.set_background_blue()
        FreeCADGui.updateGui()
        self.vis_mod(1,3)
        self.round_for_display(True)
        self.on_vis_100()                                  
        self.set_background_khaki()

      
    def on_show_hide(self):
        if self.show_flag == False:
            if self.page_number == 1.01: 
                self.page_number= 1.02
            self.set_background_blue()
            self.singles_list[0][0].setEnabled(False) ; self.singles_list[1][0].setEnabled(False) ; self.singles_list[2][0].setEnabled(False) ;  self.global_list[3][0].setEnabled(False)  # self.editor_list[2][0].setEnabled(False)
            FreeCADGui.updateGui() ; Gui.Selection.clearSelection() ; color="background-color:springgreen;"  ; self.editor_list[0][0].setStyleSheet(color)
            self.show_object = True ;  self.show_flag = True ;  color="background-color:lightgreen;"  ; self.editor_list[2][0].setStyleSheet(color)
            self.on_set_10 = False ; self.on_set_50 = False ; self.on_set_100 = False ;  self.pic_vis_at =False ; # self.editor_list[0][0].setStyleSheet(color) ;
            self.editor_list[1][0].setStyleSheet(color) ; self.editor_list[3][0].setStyleSheet(color) ;self.editor_list[4][0].setStyleSheet(color) ; self.editor_list[5][0].setStyleSheet(color)
            color="background-color:lightcyan;"; self.singles_list[1][0].setStyleSheet(color) ; self.singles_list[2][0].setStyleSheet(color) ;  # self.singles_list[0][0].setStyleSheet(color) 
            self.editor_list[3][0].setEnabled(True) ;  self.editor_list[4][0].setEnabled(True) ;  self.editor_list[5][0].setEnabled(True)
            self.round_for_display(True) 
            self.reset_display()  
            self.vis_mod(0,0)    # 0 is enter      
        else: 
            self.singles_list[0][0].setEnabled(True) ; self.singles_list[1][0].setEnabled(True) ; self.singles_list[2][0].setEnabled(True)  ;  self.editor_list[5][0].setEnabled(False) 
            self.clear_pick_buttons() ;  self.global_list[3][0].setEnabled(True) # self.editor_list[3][0].setEnabled(False) ; self.editor_list[4][0].setEnabled(False) ;
            self.vis_mod(1,0)    # 1 is exit
            self.round_for_display(False) 



    def vis_mod(self,config,mode):  #mode 1=wireframe,  2=points,  3=flatlines,,,,,,, direction 0=enter 1= exit
        #print(self.page_number )
        doc = FreeCAD.ActiveDocument
        try:
            for obj in doc.Objects:
                self.body_found = False
                ob1=obj
                if hasattr(obj.ViewObject,'PointSize')  and str(obj.TypeId) != "Sketcher::SketchObject": #  and str(type(obj)) != "<class 'PrimitivePy'>":
                    if str(obj.TypeId) != "PartDesign::Plane" and str(obj.TypeId) != "App::Origin" and str(obj.TypeId) != "App::Plane" and str(obj.TypeId) != "App::Line" and str(obj.TypeId) != "PartDesign::ShapeBinder" and str(obj.TypeId) != "PartDesign::SubShapeBinder" and str(obj.Name) != "ShapeString":  
                        if str(obj) == "<body object>": # or  str(obj) == "<PartDesign::FeatureBase>":
                            #FreeCAD.Console.PrintMessage("obj.Name = "+obj.Name+"\nobj.Label = "+obj.Label+"\nstr(obj) = "+str(obj)+"\nstr(type(obj)) = "+str(type(obj))+ "\nobj.TypeId = "+obj.TypeId  +  " \n\n")
                            if hasattr(obj,'Tip'):
                                if hasattr(obj.Tip,'Name') :  
                                    tip_name=obj.Tip.Name
                                    for ob1 in doc.Objects:
                                        if ob1.Name == tip_name:      # found the tip in the Body
                                            self.body_found =True
                                            if config == 0:
                                                self.enter_vis_edit(obj,ob1,self.body_found)
                                            else:
                                                self.exit_vis_edit(obj,mode,ob1,self.body_found)
                                            #print("done it",ob1.Name)         
                            else:
                                #FreeCAD.Console.PrintMessage("obj.Name = "+obj.Name+"\nobj.Label = "+obj.Label+"\nstr(obj) = "+str(obj)+"\nstr(type(obj)) = "+str(type(obj))+ "\nobj.TypeId = "+obj.TypeId  +  " \n\n")
                                if config == 0:
                                    self.enter_vis_edit(obj,ob1,self.body_found)
                                else:
                                    self.exit_vis_edit(obj,mode,ob1,self.body_found)
    
                        elif   str(obj) == "<Part::PartFeature>":
                            #FreeCAD.Console.PrintMessage("obj.Name = "+obj.Name+"\nobj.Label = "+obj.Label+"\nstr(obj) = "+str(obj)+"\nstr(type(obj)) = "+str(type(obj))+ "\nobj.TypeId = "+obj.TypeId  +  " \n\n")
                            if config == 0:
                                self.enter_vis_edit(obj,ob1,self.body_found)
                            else:
                                self.exit_vis_edit(obj,mode,ob1,self.body_found)   
        except:
            None  

   

    def enter_vis_edit(self,obj,ob1,body_found):
        
        if obj.ViewObject.PointSize == self.page_number or obj.ViewObject.PointSize == (self.page_number + 0.001)  and  obj.ViewObject.PointSize > 1.00:  #and obj.ViewObject.PointSize < 1.20:
            self.point_fraction = round(obj.ViewObject.PointSize ,2)
            if(self.point_fraction !=  obj.ViewObject.PointSize):     # if wireframe 
                if body_found == True:
                    ob1.ViewObject.Visibility = True
                    self.quick_pointsize = obj.ViewObject.PointSize
                    obj.ViewObject.PointSize = round(11.00 + self.quick_pointsize,3)
                    obj.ViewObject.DisplayMode  =  u"Wireframe" 
                else:
                    obj.ViewObject.Visibility = True
                    self.quick_pointsize = obj.ViewObject.PointSize
                    obj.ViewObject.PointSize = round(11.00 + self.quick_pointsize,3)
                    obj.ViewObject.DisplayMode  =  u"Wireframe"     
                #print(obj.ViewObject.PointSize,self.page_number)
            else:
                if body_found == True:
                    ob1.ViewObject.Visibility = True
                    self.quick_pointsize = obj.ViewObject.PointSize
                    obj.ViewObject.PointSize = round(11.00 + self.quick_pointsize,3)
                    obj.ViewObject.DisplayMode  = u"Points"     
                else:
                    obj.ViewObject.Visibility = True
                    self.quick_pointsize = obj.ViewObject.PointSize
                    obj.ViewObject.PointSize = round(11.00 + self.quick_pointsize,3)
                    obj.ViewObject.DisplayMode  = u"Points"     
   
        
        if obj.ViewObject.PointSize >= self.page_number and obj.ViewObject.PointSize < 1.20:        # what to do with masked
            if str(obj.TypeId) != "Part::Helix" and str(obj.TypeId) != "Part::Spiral" and str(obj.TypeId) != "Part::Line" and str(obj.TypeId) != "Part::Ellipse" and str(obj.Name) != "BaseFeature":
                if str(obj.TypeId) != "Part::RegularPolygon" and str(obj.TypeId) != "Part::Circle" :  
                  #  self.point_fraction = round(obj.ViewObject.PointSize ,2)
                 #   if(self.point_fraction !=  obj.ViewObject.PointSize):     # if wireframe        
                    if body_found == True:
                        ob1.ViewObject.Visibility = True
                        obj.ViewObject.DisplayMode  = self.dmode_text  
                    else:
                        obj.ViewObject.Visibility = True
                        obj.ViewObject.DisplayMode  = self.dmode_text  
                else:
                    if body_found == True:
                        ob1.ViewObject.Visibility = True
                        obj.ViewObject.DisplayMode  = self.dmode_text  
                    else:
                        obj.ViewObject.Visibility = True

 #       if obj.ViewObject.PointSize == 1.0:        # what to do with masked
 #           if str(obj.TypeId) != "Part::Helix" and str(obj.TypeId) != "Part::Spiral" and str(obj.TypeId) != "Part::Line" and str(obj.TypeId) != "Part::Ellipse" and str(obj.Name) != "BaseFeature":
 #               if str(obj.TypeId) != "Part::RegularPolygon" and str(obj.TypeId) != "Part::Circle" :  
 #                  # print("mm",obj.ViewObject.PointSize)
 #                   self.point_fraction = round(obj.ViewObject.PointSize ,2)
 #                   if(self.point_fraction !=  obj.ViewObject.PointSize):     # if wireframe        
 #                       if body_found == True:
 #                           ob1.ViewObject.Visibility = True
 #                           obj.ViewObject.DisplayMode  = self.dmode_text  
 #                       else:
 #                           obj.ViewObject.Visibility = True
 #                           obj.ViewObject.DisplayMode  = self.dmode_text  
 #                   else:
 #                       if body_found == True:
 #                           ob1.ViewObject.Visibility = True
 #                           obj.ViewObject.DisplayMode  = self.dmode_text  
 #                       else:
 #                           obj.ViewObject.Visibility = True                                      


  
    def exit_vis_edit(self,obj,mode,ob1,body_found):
        if mode == 0:  
            if str(obj.TypeId) != "Part::Helix" and str(obj.TypeId) != "Part::Spiral" and str(obj.TypeId) != "Part::Line" and str(obj.TypeId) != "Part::Ellipse" and str(obj.Name) != "BaseFeature":
                if str(obj.TypeId) != "Part::RegularPolygon" and str(obj.TypeId) != "Part::Circle" :  
                    if obj.ViewObject.PointSize >=12.0:  # this is flatlines 
                        obj.ViewObject.PointSize = round(obj.ViewObject.PointSize - 11.000,3)
                        #if obj.ViewObject.DisplayMode[0] == "W" :  #wireframe
                        self.point_fraction = round(obj.ViewObject.PointSize ,2)
                        if(self.point_fraction !=  obj.ViewObject.PointSize):     # if wireframe 
                            if body_found == True:
                                ob1.ViewObject.Visibility = True
                            else:
                                obj.ViewObject.Visibility = True
                        else:
                            if body_found == True:
                                ob1.ViewObject.Visibility = False
                                obj.ViewObject.DisplayMode  = self.dmode_text  
                            else:
                                obj.ViewObject.Visibility = False
                                obj.ViewObject.DisplayMode  = self.dmode_text                         

        if mode == 1:  
            if str(obj.TypeId) != "Part::Helix" and str(obj.TypeId) != "Part::Spiral" and str(obj.TypeId) != "Part::Line" and str(obj.TypeId) != "Part::Ellipse" and str(obj.Name) != "BaseFeature":
                if str(obj.TypeId) != "Part::RegularPolygon" and str(obj.TypeId) != "Part::Circle" :  
                    if obj.ViewObject.PointSize >= 1.00:  # this is flatlines 
                       # obj.ViewObject.PointSize = round(obj.ViewObject.PointSize - 11.00,3)
                        #if obj.ViewObject.DisplayMode[0] == "W" :  #wireframe
                        self.point_fraction = round(obj.ViewObject.PointSize ,2)
                        if(self.point_fraction !=  obj.ViewObject.PointSize):     # if wireframe 
                            if body_found == True:
                                ob1.ViewObject.Visibility = True
                            else:
                                obj.ViewObject.Visibility = True
                        else:
                            if body_found == True:
                                ob1.ViewObject.Visibility = True
                                obj.ViewObject.DisplayMode  = self.dmode_text  
                            else:
                                obj.ViewObject.Visibility = True
                                obj.ViewObject.DisplayMode  = self.dmode_text                
       
        if mode == 3:   # view all
            #FreeCAD.Console.PrintMessage("obj.Name = "+obj.Name+"\nobj.Label = "+obj.Label+"\nstr(obj) = "+str(obj)+"\nstr(type(obj)) = "+str(type(obj))+ "\nobj.TypeId = "+obj.TypeId  +  " \n\n")
            if str(obj.TypeId) != "Part::Helix" and str(obj.TypeId) != "Part::Spiral" and str(obj.TypeId) != "Part::Line" and str(obj.TypeId) != "Part::Ellipse" and str(obj.Name) != "BaseFeature":
                if str(obj.TypeId) != "Part::RegularPolygon" and str(obj.TypeId) != "Part::Circle"  and  obj.ViewObject.PointSize >= self.page_number:       # and str(obj.TypeId) != "App::Origin" and str(obj.TypeId) != "App::Plane" and str(obj.TypeId) != "App::Line"  and str(obj.TypeId) != "PartDesign::ShapeBinder" and str(obj.Name) != "ShapeString":  
                    obj.ViewObject.DisplayMode  = self.dmode_text  
                    #FreeCAD.Console.PrintMessage("obj.Name = "+obj.Name+"\nobj.Label = "+obj.Label+"\nstr(obj) = "+str(obj)+"\nstr(type(obj)) = "+str(type(obj))+ "\nobj.TypeId = "+obj.TypeId  +  " \n\n")
                    obj.ViewObject.PointSize = 1.00 
                    if body_found == True :
                        ob1.ViewObject.Visibility = True
                        obj.ViewObject.Visibility = True  
                    else:
                        obj.ViewObject.Visibility = True                
                                                     
################################################

    def disable_sketch_buttons(self):
        for i in range(len(self.sketch_list)):        # init options
            self.sketch_list[i][0].setEnabled(False) 
            color="background-color:lightcyan;" 
            self.sketch_list[1][0].setStyleSheet(color) 
  
    def enable_sketch_buttons(self):
        for i in range(len(self.sketch_list)):        # init options
            self.sketch_list[i][0].setEnabled(True)   #enable buttons


   ####################################################
                           
    def build_button(self,index,group):
        group[index][0] = QtGui.QPushButton(group[index][1],self)
        group[index][0].setFixedWidth(60) 
        if group[index][2] == 1:
            group[index][0].setMaximumHeight(30)           
        elif group[index][2] == 2:
            group[index][0].setMaximumHeight(18) 
        else:
            group[index][0].setMaximumHeight(15)
        color="background-color:lightcyan;" 
        group[index][0].setStyleSheet(color)
        self.lay.addWidget(group[index][0],2) 

    def disable_pick_showhide(self):
        for i in range(len(self.singles_list)):       
             self.singles_list[i][0].setEnabled(False)   
        self.show_object = False ;  self.show_flag = False 
        color="background-color:lightcyan;"  ;  self.singles_list[0][0].setStyleSheet(color) ; self.singles_list[1][0].setStyleSheet(color) ; self.singles_list[2][0].setStyleSheet(color) ; self.editor_list[0][0].setStyleSheet(color) ; self.editor_list[1][0].setStyleSheet(color)
        self.editor_list[2][0].setStyleSheet(color) ; self.editor_list[3][0].setStyleSheet(color) ;  self.editor_list[4][0].setStyleSheet(color) ; self.editor_list[5][0].setStyleSheet(color)
        self.editor_list[0][0].setEnabled(False) ; self.editor_list[1][0].setEnabled(False) ; self.editor_list[2][0].setEnabled(False) ; self.editor_list[3][0].setEnabled(False)  ; self.editor_list[4][0].setEnabled(False)  ; self.editor_list[5][0].setEnabled(False)
        self.pic_vis_at = False

    def enable_pick_showhide(self):
         for i in range(len(self.singles_list)):      
            self.singles_list[i][0].setEnabled(True)
         self.editor_list[0][0].setEnabled(True) ; self.editor_list[1][0].setEnabled(True) ; self.editor_list[2][0].setEnabled(True) ; self.editor_list[3][0].setEnabled(True) ; self.global_list[3][0].setEnabled(True)
         if self.pic_vis_at == True or self.show_object == True:
            self.set_background_blue()

                   
    def set_transparency_pick(self,data,pad):
        try:
            self.current_trans = data
            self.it_pad = pad
            self.it_pad.ViewObject.Transparency = self.current_trans
            Gui.Selection.clearSelection()
        except:
            try:
                self.current_trans = data
                self.pad.ViewObject.Transparency = self.current_trans
                Gui.Selection.clearSelection() 
            except:
                None 

    def on_color_all(self):
        Gui.Selection.clearSelection() 
        doc = FreeCAD.ActiveDocument
        for obj in doc.Objects:
            if str(obj.TypeId) != "PartDesign::Plane"  and str(obj.TypeId) != "PartDesign::ShapeBinder"  and str(obj.TypeId) != "App::Origin" and str(obj.TypeId) != "Sketcher::SketchObject" and str(obj.TypeId) != "App::Plane" and str(obj.TypeId) != "App::Line":   
                self.a=self.a +7.13 
                self.b=self.b + 2.32 
                self.c =self.c  + 5.46  
                if self.a >200.0:
                    self.a -=200
                if self.b >255.0:
                    self.b -= 255
                if self.c >225.0:
                    self.c -=225
                if hasattr(obj.ViewObject,'ShapeColor'):
                    obj.ViewObject.ShapeColor = (self.a,self.b,self.c)
                if hasattr(obj.ViewObject,'PointColor'):                            
                    obj.ViewObject.PointColor = (self.a,self.b,self.c)
      
    def process_selects(self,pnt,element):
        if  self.show_object ==  True or   self.pic_vis_at == True:      
            try:
                if element[0] == "E"  or element[0] == "F" or element[0] == "V"  or element[0] == "P"  and  self.sketch_in ==False:  #
                    self.pad = FreeCADGui.Selection.getSelection()[0]
                    Gui.Selection.clearSelection()
                    #FreeCAD.Console.PrintMessage("obj.Name = "+self.pad.Name + "\n\n")   #+"\nobj.Label = "+self.pad.Label+"\nstr(obj) = "+str(obj)+"\nstr(type(obj)) = "+str(type(self.pad.obj))+ "\nobj.TypeId = "+self.pad.TypeId  +  " \n\n")
                    if self.pad.Label == u'ShapeBinder' or self.pad.Label == u'SubShapeBinder' :
                        self.pass_this =True
                    else:
                        self.pass_this = False   

                    self.pad2=self.pad.getParentGeoFeatureGroup()     
                    if str(self.pad2) == "<body object>" or  str(self.pad2) == "<PartDesign::FeatureBase>" or  str(type(self.pad2)) == "<PartDesign::Feature>" :                          
                        self.pad3=self.pad2
                        self.is_body=True   
                    else:
                        self.pad3=self.pad
                        self.is_body= False

                    if hasattr(self.pad.ViewObject,'ControlPoints'):   # if it's a helix of something
                        self.ct_points=True      
                    else :
                        self.ct_points =False

                    if self.pic_vis_at == True  and  self.ct_points == False:
                        self.set_transparency_pick(self.pic_vis_at_value,self.pad3)   #### we use pad3 because it's a body and not the feature
                        self.pass_this = True

                    if self.is_body == True:         ############    if body object
                        self.pad = self.pad2

                    self.pad9=self.pad.getParentGeoFeatureGroup()   #  find the Part name if there is one
                    if self.pad9 != 'None'  and  self.object_part_flag ==False  and  self.pass_this ==  False  and  self.part_lock ==False and self.pad9.Type != "Assembly4 Model":   # if not a Part and button selection and not a 
                      #  Gui.Selection.clearSelection() 
                        self.pass_this = True
                        self.set_part_vis(self.pad9,self.pad)  # this is a branch off to edit mode

           #############  --------------------------------   ########### start of processing
                    if  self.show_object ==  True and  self.pass_this ==  False and  self.ct_points == False :
                      #  Gui.Selection.clearSelection()  
                    
                        if self.pad.ViewObject.PointSize  < 12:   #>=0.99 and  self.pad.ViewObject.PointSize <= 1.50 :
                            if self.mode_wireframe == True:                
                                self.pad.ViewObject.DisplayMode  =  u"Wireframe"
                                self.pad.ViewObject.PointSize  =  round(11.001 + self.page_number, 3)  #self.small_point_size   put number here
                            else:
                                self.pad.ViewObject.PointSize  =  round(11.00 + self.page_number,2)   #self.small_point_size
                                self.pad.ViewObject.DisplayMode  = u"Points"
                        else:
                            self.pad.ViewObject.PointSize  =  1.0  #self.page_number   #self.small_point_size
                            self.pad.ViewObject.DisplayMode  = self.dmode_text 
                          
                        self.pad.ViewObject.PointColor = self.pad.ViewObject.ShapeColor
                
             #   Gui.Selection.clearSelection()               
            except:
                None

    def set_part_vis(self, address,target_obj):
        self.parent =address
        if target_obj.ViewObject.PointSize <1.20:
            self.my_pointsize = 12.0
        else:
            self.my_pointsize = 1.0
        for obj in address.OutList:
            if hasattr(obj.ViewObject,'PointSize'): # and str(type(obj)) != "<class 'PrimitivePy'>":
                if self.my_pointsize >= 12.0: 
                    if self.mode_wireframe == True :                
                        obj.ViewObject.DisplayMode  =  u"Wireframe"
                        obj.ViewObject.PointSize  =  round(11.001 +self.page_number,3)   #self.small_point_size   put number here
                    else:
                        obj.ViewObject.PointSize  =  round(11.00 + self.page_number,2)   #self.small_point_size
                        obj.ViewObject.DisplayMode  = u"Points"
                else:
                    if self.mode_wireframe == True :                
                        obj.ViewObject.DisplayMode  =  u"Wireframe"
                        obj.ViewObject.PointSize  =  1.0  #round(self.page_number + .001,3)   #self.small_point_size   put number here
                    else:
                        obj.ViewObject.PointSize  =  1.0  #round(self.page_number,2)   #self.small_point_size
                        if str(obj.TypeId) != "Part::Helix" and str(obj.TypeId) != "Part::Spiral" and str(obj.TypeId) != "Part::Line" and str(obj.TypeId) != "Part::Ellipse" and str(obj.Name) != "BaseFeature":
                            if str(obj.TypeId) != "Part::RegularPolygon" and str(obj.TypeId) != "Part::Circle": 
                                obj.ViewObject.DisplayMode  = self.dmode_text 
             

    
   ####################### ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class SelObserver:
  
    def addSelection(self,document, object, element, position):
 
        visCB.process_selects(position,element)

##########################^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       

s=SelObserver()
FreeCADGui.Selection.addObserver(s)

visCB = CB_ToolBox()
visCB.show()
