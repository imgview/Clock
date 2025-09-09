#PyBinClockk
#iphone style
#Ibnu Wahyudi
#Nov 14, 2022
#Nov 17, 2022

#Update : Aug 31, 2024
#kivy 2.2.1
#kivymd 1.2.0

__version__ = "1.11.17"

import kivy
import os, time
from kivy.core.text import Label as CoreLabel
from kivy.clock import Clock
from kivy.graphics import *
from kivy.properties import *
from kivy.factory import *
from kivymd.toast import toast
from kivymd.uix.bottomsheet import *
from kivymd.uix.widget import *
from kivymd.app import MDApp
from kivymd.uix.boxlayout import *
from kivymd.uix.gridlayout import *
from kivymd.uix.floatlayout import *
from kivymd.uix.screen import *
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.button import *
from kivymd.color_definitions import colors, palette

from kivymd.uix.screen import MDScreen

#o = open("/sdcard/colors.txt","w")
#o.write(str(colors))
#o.close()

ts = time.strftime
t = time.time()
style = ["Light", "Dark"]
#palette = ["Red", "Green", "Blue", "Pink", "Purple", "Teal", "Orange", "DeepOrange", "Indigo", "LightBlue", "Cyan", "LightGreen", "Lime", "Yellow", "Amber", "Gray"]


conf = {"style": "Dark", "palette": "LightBlue","seconds": True, "numbers": False, "captions": False, "daemon": False, "auto": False}
img = ["img/"+i for i in os.listdir("img/")]

class BinaryClock(MDWidget):
    tile = NumericProperty(140)
    clocksize = ListProperty()
    
    def __init__(self, **kwargs):
        super(BinaryClock, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        Clock.schedule_interval(self.update_canvas, .5)
        
    def update_canvas(self, *args):
        line = 10
        self.canvas.clear()
        with self.canvas:
            if conf["style"] == "Dark":
                Color(0, 0, 0, 1)
            else:
                Color(1, 1, 1, 1)
            Rectangle(size=self.size)
            self.__loopCircle()
            self.__updateTime()
    
    def __updateTime(self):
        H, M, S = int(ts("%H")), int(ts("%M")), int(ts("%S"))
        self.__draw(self.splitClock(H, M, S))
        
    
    def splitClock(self, h, m, s):
        return h, m, s
    
    def toBin(self, x):
       if int(x)==0: return [0,0,0,0,0,0]
       n = ''
       while int(x) >0:
            y = str((int(x) % 2))
            n = y + n
            x = int((int(x) / 2))
       return [int(x) for x in '%06d'%int(n)]

    def __cetak(self, x, num):
        im = [self._im(), self._im(conf["palette"].lower())]
        for i in range(len(x)):
            pos_x = i
            pos_y = num
            pos = ( self.mx+(pos_x*self.tile)   ,    self.my+self.pos[1]+(pos_y*self.tile))
            Rectangle(source=im[int(x[i])], pos=pos, size=self.clocksize)
    
    def __draw(self, c):
        if conf["seconds"]:
            self.__cetak(self.toBin(c[2]), 0)
        self.__cetak(self.toBin(c[1]), 2)
        self.__cetak(self.toBin(c[0]), 4)
        
    def __loopCircle(self):
        self.clocksize = (self.tile, self.tile)
        lbl_color = main.theme_cls.primary_light
        xy = 6
        self.mx = (self.size[0]-(self.tile*xy))/2
        self.my = (self.size[1]-(self.tile*xy))/2
        for x in range(xy):
            #draw vertical circle list
            for y in range(xy):
                x1 = self.mx+x*self.tile
                y1 = self.my+self.pos[1]+(y*self.tile)
                Color(1, 1, 1, 1)
                #genap
                if y%2==0:
                    if y == 0:
                        if conf["seconds"] == True:
                            Rectangle(source=self._im(), size=self.clocksize, pos=(x1, y1))
                    else:
                        Rectangle(source=self._im(), size=self.clocksize, pos=(x1, y1))
            
            #core label
            th = [ts("%S"),"", ts("%M"),"", ts("%H"), ""][x]
            tb = ["32", "16", "08", "04", "02", "01"][x]
            mb = CoreLabel(text=tb, font_size=round(self.tile*.4), color=(lbl_color), bold=True)
            mh = CoreLabel(text=th, font_size=round(self.tile*.4), color=(lbl_color), bold=True)
            mb.refresh(); mh.refresh()
            txh = mh.texture; txb = mb.texture
            b_size = list(txb.size); h_size = list(txh.size)
            
            #binary decimal
            if conf["numbers"]==True:
                x1 = self.mx+(x*self.tile)+(b_size[0]*.4)
                y1 = (self.my+self.pos[1])+(5*self.tile)
                Rectangle(texture=txb, size=b_size,  pos=(x1, y1) )
            #digit clock
            if x%2==0:
                x1 = self.mx-(1*self.tile)+(h_size[0]*.4)
                y1 = (self.my+self.pos[1])+(x*self.tile)+(self.tile/4)
                if x == 0:
                    if conf["captions"] == True & conf["seconds"] == True:
                        Rectangle(texture=txh, size=h_size,  pos=(x1, y1) )
                else:
                    if conf["captions"]==True:
                        Rectangle(texture=txh, size=h_size,  pos=(x1, y1) )
        
    def _im(self, clr=""):
        if clr == "":
            c = conf["palette"]
            if c in ["Red", "Orange", "DeepOrange", "Pink", "Amber", "Yellow", "Lime", "Brown"]:
                clr = "red-outline"
            else: clr = "blue-outline"
        clr = clr.lower()
        try:
            im = img[img.index(os.path.join("img/", f"{clr}.png"))]
        except:
            im = img[img.index(os.path.join("img/", f"white.png"))]
        return im
              
        
class rootWindow(MDScreen):
    pass


class rightCheckbox(IRightBodyTouch, MDSwitch):
    pass

#class ItemButtonSheet(MDIconButton):
#    pass

class binaryApp(MDApp):
    captions = conf["captions"]
    numbers = conf["numbers"]
    seconds = conf["seconds"]
    auto = conf["auto"]
    COLORS = len(palette)
    popup = None
    sett = 0
    #tmp_popup = None
        
    def build(self):
        self.popup = ObjectProperty()
        self.float = ObjectProperty()
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = conf["style"]
        self.theme_cls.primary_palette = conf["palette"]
        self.on_settings_popup()
        #self._init_grid_color()
        return rootWindow()
        
    def switch_theme(self):
        self.theme_cls.primary_palette = conf["palette"]
        
    def on_grid_selected(self, *args):
        color = args[0].text
        conf["palette"] = color
        self.switch_theme()
        toast(f"Color {color} selected")
        
        
    def on_selected_grid(self, *args):
        clr = args[0]
        if clr == "Deep": clr = "DeepOrange"
        conf["palette"] = clr
        self.switch_theme()
        toast(f"Color {clr} selected")

    def on_settings_popup(self):
        #self._init_grid_color()
        #self.popup.open()
        #self.float = Factory.floatWindow()
        pass
        
    def _init_grid_color(self):
        """This function temporarily disabled due to unsupported with latest kivy/kivyMD update"""
        t = time.time()
        float = Factory.floatWindow()
        #mainscr = Factory.rootWindow()
        #mainscr.add_widget(screen)
        grid = float.ids.gridcolor
        btn_list = []
        for i in range(len(palette)):
            #time.sleep(.1)
            #btn = ObjectProperty()
            color = palette[i]
            btn = Factory.ItemButtonSheet(
                    text=color,
                    md_bg_color=f'#{colors[color]["500"]}',
                    on_release = lambda x: self.on_grid_selected(x))
            btn_list.append(color)
            grid.add_widget(btn)
            #toast(color)
        #self.popup = MDCustomBottomSheet(screen=screen, radius=60, radius_from="top")
        #self.popup = MDCustomBottomSheet(radius=60, radius_from="top")
        
        toast("Loaded in %.02f seconds"%(time.time()-t))
        
    
    #theme switch
    def on_style_active(self, checkbox, value):
        if value: conf["style"] = style[1]
        else: conf["style"] = style[0]
        self.theme_cls.theme_style = conf["style"]
    #caption switch
    def on_captions_active(self, checkbox, value):
        if value: conf["captions"] = True
        else: conf["captions"] = False
        self.captions = conf["captions"]
    #number switch
    def on_numbers_active(self, checkbox, value):
        if value: conf["numbers"] = True
        else: conf["numbers"] = False
        self.numbers = conf["numbers"]
    #second switch
    def on_seconds_active(self, checkbox, value):
        if value: conf["seconds"] = True
        else: conf["seconds"] = False
        self.seconds = conf["seconds"]
    def on_auto_active(self, checkbox, value):
        if value:
            self.auto = False
            toast("Feature not available now")


main = binaryApp()
if __name__ == "__main__":
    main.run()
    