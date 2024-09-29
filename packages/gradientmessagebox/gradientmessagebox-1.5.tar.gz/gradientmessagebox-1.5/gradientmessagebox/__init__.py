"""A very simple tkinter prompt window with an animated gradient background, By: Fibo Metavinci"""

__version__ = "1.5"

import threading
import tkinter
from tkinter import font
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from pathlib import Path
import sys
import time
from colour import Color
import pyperclip
import webbrowser
import os

FILE_PATH = Path(__file__).parent


class GradientFrame(tkinter.Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, color1="red", color2="black", direct='+x', animated=False, speed=50, stretch=2, **kwargs):
        tkinter.Canvas.__init__(self, parent, **kwargs)
        self._width = kwargs.get('width')
        self._height = kwargs.get('height')
        self._color1 = color1
        self._color2 = color2
        self._animated = animated
        self._direct = direct
        self._midColor = None
        self._limit = self._width
        self._active = False
        self._speed = speed
        self._stretch = stretch
        self._root = None
        if 'y' in self._direct:
            self._limit = self._height

        self.colors = list(Color(self._color1).range_to(Color(self._color2), self._limit))
        if '-' in self._direct:
            c1 = self._color2
            c2 = self._color1

            self.colors = list(c1.range_to(c2, self._limit))

        if self._animated:
            self._thread = threading.Thread(target=self.Animate)
            self._thread.setDaemon(True)
            self._draw_gradient()
            self._active = True
            self.Play()
        else:
            self.bind("<Configure>", self._draw_gradient)

    def SetRoot(self, root):
        self._root = root

    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")

        for i in range(self._limit):
            color = "%s" % self.colors[i]
            if 'y' in self._direct:
                self.create_line(0,i,self._width,i, tags=("gradient",), fill=color)
            else:
                self.create_line(i,0,i,self._height, tags=("gradient",), fill=color)
        self.lower("gradient")

    def Stop(self):
        self._active = False
        self._root.after_cancel(self.Animate)

    def Play(self):
        c1 = self._color1
        c2 = self._color2
        if '-' in self._direct:
            c1 = self._color2
            c2 = self._color1

        colors1 = list(c1.range_to(c2, int(self._limit*self._stretch)))
        colors2 = list(c2.range_to(c1, int(self._limit*self._stretch)))

        self.colors = colors1+colors2
        self._thread.start()

    def Animate(self):
        if self and self._active:
            try:
                self.colors.append(self.colors.pop(0))
                self._draw_gradient()
                self.after(self._speed, self.Animate)
            except:
                print('')


class WidgetConfig:
    def __init__(self, padding=(10, 10), font='Fira Sans', fontSize=12, ):
        self.padding = padding
        self.font = (font, fontSize)
        self.h1 = (font, fontSize+9)
        self.h1_outline = (font, fontSize+9, 'bold')
        self.h2 = (font, fontSize+6)
        self.h2_outline = (font, fontSize+6, 'bold')
        self.h3 = (font, fontSize+3)
        self.h3_outline = (font, fontSize+3, 'bold')

class Config:
    def __init__(self, width=450, height=300, title=""):
        self.width = width
        self.height = height
        self.title = title
        self.widgetConfig = None

    def DefaultWidgetConfig(self):
        self.widgetConfig = WidgetConfig()

    def CustomWidgetConfig(self, padding, font, fontSize):
        self.widgetConfig = WidgetConfig(padding, font, fontSize)

class ColorConfig(Config):
    def __init__(self, width=450, height=300, color1="#00ffff", color2="#ffa500", alpha=1.0, saturation=1.0, direct='+x', hasFrame=True):
        Config.__init__(self, width, height)
        self.color1 = Color(color1)
        self.color2 = Color(color2)
        self.alpha = alpha
        self.saturation = saturation
        self.direct = direct
        self.hasFrame = hasFrame
        self.animated = False
        self.speed = 0
        self.stretch = 1
        self.fg_color = Color(self.color1.hex_l)
        self.bg_color = Color(self.color2.hex_l)
        self.txt_color = None
        self.msg_color = None
        self.text_outline_color = None
        limit = self.width
        if 'y' in direct:
            limit = self.height
        colors = list(self.bg_color.range_to(self.fg_color, limit))
        self.mg_color = colors[int(len(colors)/2)]
        self.path = None
        self.file = None
        self.icon_path = None
        self.icon_file = None
        self.entry_text = None
        self.file_types = []

    def set_title_text(self, text):
        self.title = text

    def set_file_select_types(self, arr):
        '''pass array of file types like this: [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]'''
        self.file_types = arr

    def default_entry_text(self, text):
        self.entry_text = text

    def custom_txt_color(self, color):
        self.txt_color = Color(color)

    def custom_msg_color(self, color):
        self.msg_color = Color(color)

    def custom_txt_outline_color(self, color):
        self.txt_outline_color = Color(color)

    def invert(self):
        self.fg_color = Color(self.color2.hex_l)
        self.bg_color = Color(self.color1.hex_l)

    def fg_luminance(self, value):
        self.fg_color.luminance = value

    def bg_luminance(self, value):
        self.bg_color.luminance = value

    def mg_luminance(self, value):
        self.mg_color.luminance = value

    def gradient_luminance(self, value):
        self.color1.luminance = value
        self.color2.luminance = value

    def fg_saturation(self, value):
        self.fg_color.saturation = value

    def bg_saturation(self, value):
        self.bg_color.saturation = value

    def mg_saturation(self, value):
        self.mg_color.saturation = value

    def gradient_saturation(self, value):
        self.color1.saturation = value
        self.color2.saturation = value

    def swap_mg_for_bg(self):
        bg = self.bg_color.hex_l
        mg = self.mg_color.hex_l
        self.bg_color = Color(mg)
        self.mg_color = Color(bg)

    def swap_mg_for_fg(self):
        fg = self.fg_color.hex_l
        mg = self.mg_color.hex_l
        self.bg_color = Color(mg)
        self.mg_color = Color(fg)

    def imagery(self, path, icon_path=None, useImgSize=False):
        self.path = path
        self.file = Image.open(self.path)
        if icon_path != None:
            self.icon_path = icon_path
        if useImgSize:
            self.width, self.height = self.file.size

    def animation(self, speed=50, stretch=2):
        self.speed = speed
        self.stretch = stretch
        self.animated = True

    def has_frame(self, showFrame):
        self.hasFrame = showFrame


class BaseWindow:
    def __init__(self, config):
        self.path = None
        self.img = None
        self.hasImg = False
        self.width = config.width
        self.height = config.height
        self.title = config.title
        self.color1 = config.color1
        self.color2 = config.color2
        self.saturation = config.saturation
        self.animated = config.animated
        self.speed = config.speed
        self.stretch = config.stretch
        self.fg = config.fg_color
        self.msg_color = config.fg_color
        self.txt_color = config.fg_color
        self.txt_outline_color = config.bg_color
        if config.txt_color != None:
            self.txt_color = config.txt_color
        if config.text_outline_color != None:
            self.txt_outline_color = config.text_outline_color
        if config.msg_color != None:
            self.msg_color = config.msg_color
        self.bg = config.bg_color
        self.mg = config.mg_color
        self.alpha = config.alpha
        self.direct = config.direct
        self.hasFrame = config.hasFrame
        self.entry_text = config.entry_text
        self.file_types = config.file_types
        self.file = None
        self.path = None
        self.icon_path = None
        self.icon_file = None
        self.hasImg = True

        if config.path != None:
            self.file = config.file
            self.path = config.path
            self.icon_path = config.icon_path
            self.icon_file = config.icon_file
            self.hasImg = True

        if config.widgetConfig is None:
            config.DefaultWidgetConfig()

        self.widgetConfig = config.widgetConfig
        self.padding = self.widgetConfig.padding
        self.font = self.widgetConfig.font
        self.h1 = self.widgetConfig.h1
        self.h1_outline = self.widgetConfig.h1_outline
        self.h2 = self.widgetConfig.h2
        self.h2_outline = self.widgetConfig.h2_outline
        self.h3 = self.widgetConfig.h3
        self.h3_outline = self.widgetConfig.h3_outline

        self.btn_height = 50

        self.root = None
        self.canvas = None
        self.btns = []
        self.text = None
        self.entry = None
        self.btn1 = None
        self.dropdown = None
        self.msg = ''
        self.animate = False

    def add_lambda_btn(self, btn_txt, method, *args):
        btn = tkinter.Button(self.canvas, text=btn_txt, command= lambda var=args: method(var))
        self.btns.append(btn)
        return btn

    def add_choice_btn(self, btn_txt):
        btn = tkinter.Button(self.canvas, text=btn_txt)
        self.btns.append(btn)
        return btn

    def _add_link_button(self, link, y):
        btn = tkinter.Button(self.canvas, text=link, command= lambda: webbrowser.open_new(link))
        self.btns.append(btn)
        btn.place(x = self.width/2-((self.width/2)*0.95), y = y, height = self.btn_height, relwidth = 0.95)

        self.configure_btns()

    def configure_btns(self):
        for btn in self.btns:
            hlt_bg = Color(self.bg.hex_l)
            hlt_fg = Color(self.txt_color.hex_l)
            hlt_bg.luminance = 0.45
            hlt_fg.luminance = 0.75
            btn.configure(fg=self.txt_color.hex_l, bg=self.bg.hex_l, highlightthickness=0, activebackground=hlt_bg.hex_l, activeforeground=hlt_fg.hex_l, font=self.h3, bd=0)

    def add_entry(self, multi=False, enabled=True):
        bg = Color(self.bg.hex_l)
        fg = Color(self.txt_color.hex_l)
        bg.luminance = 0.75
        fg.luminance = 0.55
        ent = None
        entry_type = 'Text'
        if multi:
            self.entry = tkinter.Text(self.canvas, bg=bg.hex_l,fg=fg.hex_l,  bd=0, highlightthickness=0, font=self.font)
        else:
            entry_type = 'Entry'
            self.entry = tkinter.Entry(self.canvas, bg=bg.hex_l,fg=fg.hex_l,  bd=0, highlightthickness=0, font=self.font)

        if self.entry_text != None:
            if entry_type == 'Text':
                self.entry.tag_configure("tag_center", justify='center')
                self.entry.insert('0.0', self.entry_text)
                self.entry.tag_add("tag_center", "1.0", "end")
            else:
                self.entry.insert(tkinter.END, self.entry_text)

        return self.entry  

    def entry_to_dict(self, dict_key):
        data = self.entry.get()
        if data:
            d, key = dict_key
            d[key] = data
            self.top.destroy()

    def add_dropdown(self, arr):
        self.dropdown_val = tkinter.StringVar(self.root)
        self.dropdown_val.set(arr[0]) # default value
        hlt_bg = Color(self.bg.hex_l)
        hlt_fg = Color(self.txt_color.hex_l)
        hlt_bg.luminance = 0.45
        hlt_fg.luminance = 0.75

        self.dropdown = tkinter.OptionMenu(self.canvas, self.dropdown_val, *arr)
        self.dropdown.configure(bg=self.txt_color.hex_l, fg=self.bg.hex_l, highlightthickness=0, activebackground=hlt_fg.hex_l, activeforeground=hlt_bg.hex_l, font=self.h3, bd=0)
        self.dropdown['menu'].configure(bg=self.txt_color.hex_l, fg=self.bg.hex_l, activebackground=hlt_fg.hex_l, activeforeground=hlt_bg.hex_l, font=self.h3, bd=0)

        self.dropdown.pack()

        return self.dropdown

    def update_canvas_text(self, text):
        self.canvas.itemconfigure(self.text, text=text)

    def start_msg_animation(self, *args):
        thread = threading.Thread(target=self.msg_animation, args=args)
        thread.setDaemon(True)
        thread.start()

    def msg_animation(self, animation=['  -  ', '  /  ', '  |  ', '  \\  '], appendMsg=True):
        i = 0
        while self.animate:
            anim = animation[i % len(animation)]
            if appendMsg:
                self.update_canvas_text( anim + f"{self.msg}" )
            else:
                self.update_canvas_text( anim )
            time.sleep(0.25)
            i += 1

    def _center_window(self, win):
        win.wait_visibility() # make sure the window is ready
        x = ((win.winfo_screenwidth()//2) - (win.winfo_width())) // 2
        y = (win.winfo_screenheight() - (win.winfo_height())) // 2
        win.geometry(f'+{x}+{y}')

    def _Show(self):
        self.root = tkinter.Tk()
        if self.icon_path != None:
            self.icon_file = tkinter.PhotoImage(file=self.icon_path)
            self.root.iconphoto(True, self.icon_file)
            self.root.iconify()
        self.root.geometry('1x1+10+10')
        win = self.root.title(self.title)
        self.root.pack_propagate(0)
        self._center_window(self.root)
        self.root.overrideredirect(True)
        self.window = tkinter.Toplevel(width=self.width, height=self.height)

        self.root.overrideredirect(True)
        self.window.resizable(width=False, height=False)
        self.window.pack_propagate(0)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        if not self.hasFrame:
            self.window.overrideredirect(True)

        self._center_window(self.window)
        self.canvas = GradientFrame(self.window, self.color1, self.color2, self.direct, self.animated, self.speed, self.stretch, width=self.width, height=self.height, bd=0,
                   highlightthickness=0, relief="ridge")
        self.canvas.pack(expand=True, fill='both')
        self.canvas.SetRoot(self.root)

        if self.hasImg and self.path != None:
            self.img = tkinter.PhotoImage(file=self.path, format='png')
            self.canvas.create_image(self.width/2, self.height/2, image=self.img)

        self.window.wm_attributes("-alpha", self.alpha)
        if self.animate:
            self.start_msg_animation()

    def Close(self):
        print('close')
        self.animate = False
        self.canvas.Stop()
        self.root.after_cancel(self.canvas.Animate)
        sys.stdout.flush()
        return

    def ForceClose(self):
        self.animate = False
        self.canvas.Stop()
        self.root.after_cancel(self.canvas.Animate)
        self.root.destroy()
        sys.stdout.flush()
        return

    def on_close(self):
        self.animate = False
        self.canvas.Stop()
        self.root.destroy()

        
class DebugFontWindow(BaseWindow):
    def __init__(self, config):
        BaseWindow.__init__(self, config)
    def Show(self):
        self._Show()
        fonts=list(font.families())
        fonts.sort()
        listnumber = 1
        for item in self.fonts:
            label = "listlabel" + str(listnumber)
            label = tkinter.Label(self.canvas,text=item,font=(item, 16)).pack()
            listnumber += 1


class BaseConfigWindow:
    def __init__(self):
        self.config = ColorConfig(width=400, height=350, color1="#4ed8a7", color2="#cf5270", alpha=1.0, saturation=1.0, direct='+x', hasFrame=True)
        self.config.animation(speed=20, stretch=4)
        self.window = None

    def configure(self, config):
        self.config = config

    def dimensions(self, width, height):
        self.config.width = width
        self.config.height = height

    def imagery(self, bg_img, logo_img):
        self.config.imagery(bg_img, logo_img)

    def color1(self, color):
        self.config.color1 = color

    def color2(self, color):
        self.config.color2 = color

    def alpha(self, alpha):
        self.config.alpha = alpha

    def invert(self):
        self.config.invert()

    def swap_fg_for_bg(self):
        self.config.swap_fg_for_bg()

    def swap_mg_for_bg(self):
        self.config.swap_mg_for_bg()

    def swap_bg_for_fg(self):
        self.config.swap_bg_for_fg()

    def swap_mg_for_fg(self):
        self.config.swap_mg_for_fg()

    def fg_saturation(self, saturation):
        self.config.fg_saturation(saturation)

    def bg_saturation(self, saturation):
        self.config.bg_saturation(saturation)

    def mg_saturation(self, saturation):
        self.config.mg_saturation(saturation)

    def fg_luminance(self, luminance):
        self.config.fg_saturation(luminance)

    def bg_luminance(self, luminance):
        self.config.bg_luminance(luminance)

    def mg_luminance(self, luminance):
        self.config.mg_luminance(luminance)

    def custom_txt_color(self, color):
        self.config.custom_txt_color(color)

    def custom_msg_color(self, color):
        self.config.custom_msg_color(color)

    def saturation(self, saturation):
        self.config.saturation = saturation

    def has_frame(self, showFrame):
        self.config.has_frame(showFrame)

    def default_entry_text(self, text):
        self.config.default_entry_text(text)

    def set_title_text(self, text):
        self.config.set_title_text(text)

    def set_file_select_types(self, arr):
        '''pass array of file types like this: [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]'''
        self.config.set_file_select_types( arr )


class ThreadedWindow(BaseConfigWindow):
    def __init__(self, window, *args):
        BaseConfigWindow.__init__(self)
        self._window = window
        self.args = args

    def _init(self):
        self.window = self._window(self.config)
        self.thread = threading.Thread(target=self.window.Show, args=self.args)
        self.thread.setDaemon(True)

    def Show(self):
        self.thread.start()
        
    def Close(self):
        self.window.Close()

    def update_canvas_text(text):
        self.window.update_canvas_text(text)


class BasePresetThreadedWindow(ThreadedWindow):
    def __init__(self, window, *args):
        self.config = ColorConfig(width=400, height=350, color1="#4ed8a7", color2="#cf5270", alpha=1.0, saturation=1.0, direct='+x', hasFrame=True)
        self.config.animation(speed=20, stretch=4)
        ThreadedWindow.__init__(self, window, args)


class PresetThreadedWindow(BasePresetThreadedWindow):
    def __init__(self, window, msg, *args):
        BasePresetThreadedWindow.__init__(self, window, args)
        self.msg = msg

    def init(self):
        self._init()
        self.window.msg = self.msg


class PresetLoadingMessage(PresetThreadedWindow):
    def __init__(self, msg, *args):
        PresetThreadedWindow.__init__(self, TextWindow, args)
        self.dimensions(width=500, height=40)
        self.has_frame(showFrame=False)
        self.msg = msg

    def Play(self):
        self.init()
        self.window.animate = True
        self.Show()
        return self

    def Stop(self):
        self.window.animate = False
        self.Close()

class PresetImageBgMessage(PresetThreadedWindow):
    def __init__(self, msg, bg_img, logo_img, *args):
        PresetThreadedWindow.__init__(self, TextWindow, args)
        self.dimensions(width=450, height=300)
        self.has_frame(showFrame=False)
        self.imagery(bg_img, logo_img)
        self.msg = msg

    def Play(self):
        self.init()
        self.window.animate = True
        self.Show()
        return self

    def Stop(self):
        self.window.animate = False
        self.Close()


class PresetDictWindowBase(BaseConfigWindow):
    def __init__(self, _window, dictionary):
        BaseConfigWindow.__init__(self)
        self._window = _window
        self.window = None
        self.dict = dictionary

    def _init(self):
        self.window = self._window(self.config, self.dict)


class PresetMessageWindowBase(BaseConfigWindow):
    def __init__(self, _window, msg, link=False):
        BaseConfigWindow.__init__(self)
        self._window = _window
        self.window = None
        self.msg = msg
        self.link = link

    def _init(self):
        self.window = self._window(self.config, self.msg, self.link)


class PresetWindowBase(BaseConfigWindow):
    def __init__(self, _window, msg, b_accept, b_decline, entry, horizontal):
        BaseConfigWindow.__init__(self)
        self._window = _window
        self.window = None
        self.msg = msg
        self.b_accept = b_accept
        self.b_decline = b_decline
        self.entry = entry
        self.horizontal = horizontal

    def _init(self):
        self.window = self._window(self.config, self.msg, self.b_accept, self.b_decline, self.entry, self.horizontal)

    def vertical_btns(self):
        self.horizontal = False


class PresetPromptWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='OK'):
        PresetWindowBase.__init__(self, ChoiceWindow, msg, b_accept, 'Close', False, True)
        self.dimensions(width=450, height=250)
        self.has_frame(showFrame=True)

    def Prompt(self):
        self._init()
        return self.window.Prompt()


class PresetWidePromptWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='OK'):
        PresetWindowBase.__init__(self, ChoiceWindow, msg, b_accept, 'Close', False, True)
        self.dimensions(width=950, height=300)
        self.has_frame(showFrame=True)

    def Prompt(self):
        self._init()
        return self.window.Prompt()


class PresetLinkWindow(PresetMessageWindowBase):
    def __init__(self, msg):
        PresetMessageWindowBase.__init__(self, MessageWindow, msg, True)
        self.dimensions(width=950, height=250)
        self.has_frame(showFrame=True)

    def Prompt(self):
        self._init()
        return self.window.Prompt()


class PresetChoiceWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='OK', b_decline='CANCEL'):
        PresetWindowBase.__init__(self, ChoiceWindow, msg, b_accept, b_decline, False, True)
        self.dimensions(width=450, height=250)
        self.has_frame(showFrame=True)

    def Ask(self):
        self._init()
        return self.window.Ask()


class PresetChoiceEntryWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='OK', b_decline='CANCEL'):
        PresetWindowBase.__init__(self, ChoiceWindow, msg, b_accept, b_decline, True, True)
        self.dimensions(width=450, height=100)
        self.has_frame(showFrame=True)

    def Ask(self):
        self._init()
        return self.window.Ask()


class PresetFileSelectWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='BROWSE'):
        PresetWindowBase.__init__(self, FileSelectWindow, msg, b_accept, 'CANCEL', True, True)
        self.dimensions(width=450, height=250)
        self.has_frame(showFrame=True)

    def FileSelect(self):
        self._init()

        return self.window.FileSelect()


class PresetDropDownWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='OK'):
        PresetWindowBase.__init__(self, ChoiceWindow, msg, b_accept, 'CANCEL', True, True)
        self.dimensions(width=450, height=250)
        self.has_frame(showFrame=True)

    def DropDown(self, arr):
        self._init()
        return self.window.DropDown(arr)


class PresetChoiceMultilineEntryWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='OK', b_decline='CANCEL'):
        PresetWindowBase.__init__(self, MultiTextChoiceWindow, msg, b_accept, b_decline, True, True)
        self.dimensions(width=450, height=250)
        self.has_frame(showFrame=True)
        self.msg = msg

    def Ask(self):
        self._init()
        return self.window.Ask()


class PresetCopyTextWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='COPY', b_decline='CANCEL'):
        PresetWindowBase.__init__(self, CopyTextWindow, msg, b_accept, b_decline, True, True)
        self.dimensions(width=450, height=250)
        self.has_frame(showFrame=True)

    def Ask(self):
        self._init()
        return self.window.Ask()


class PresetUserPasswordWindow(PresetWindowBase):
    def __init__(self, msg, b_accept='GO', b_decline='CANCEL'):
        PresetWindowBase.__init__(self, UserPasswordWindow, msg, b_accept, b_decline, True, True)
        self.dimensions(width=450, height=250)
        self.has_frame(showFrame=True)
        self.msg = msg

    def Ask(self):
        self._init()
        return self.window.Ask()


class PresetMultiButtonWindow(PresetDictWindowBase):
    def __init__(self, btn_dict):
        PresetDictWindowBase.__init__(self, MultiButtonWindow, btn_dict)
        self.dimensions(width=450, height=250)
        self.has_frame(showFrame=True)

    def Show(self):
        self._init()
        return self.window.Show()


class TextWindow(BaseWindow):
    def __init__(self, config):
        BaseWindow.__init__(self, config)

    def Show(self, msg):
        self._Show()
        x = self.width/2
        y = self.height/2
        rely = 0.333
        relHeight = 0.25
        inc=1
        #if self.msg is set, it is used
        if len(self.msg) > 0:
            msg = self.msg
        self.text = self.canvas.create_text(x, y, text=msg, fill=self.msg_color.hex_l, font=self.h3, anchor='center')
        self.root.mainloop()
        return self


class MultiButtonWindow(BaseWindow):
    def __init__(self, config, btn_dict):
        BaseWindow.__init__(self, config)
        #For dynamic height
        self.btn_dict = btn_dict
        self.methods = {}
        self.max_height = 900
        self.buffer = 5
        self.line_spacing = 5
        self.height = self.buffer+(self.line_spacing+self.btn_height)*len(self.btn_dict)
        self.btn_y = self.buffer/2

    def _btn_press(self, name):
        key = name[0]
        self.ForceClose()
        time.sleep(0.7)
        self.methods[key]()


    def Show(self):
        self._Show()
        i=0
        for name, method in self.btn_dict.items():
            if i > 0:
                self.btn_y += self.btn_height
                self.btn_y += self.line_spacing

            btn = self.add_lambda_btn(name, self._btn_press, name)
            self.methods[name] = method
            btn.place(x = self.width/2-((self.width/2)*0.8), y = self.btn_y, height = self.btn_height, relwidth = 0.75)
            i+=1

        self.configure_btns()
        self.root.mainloop()
        return self


class MessageWindow(BaseWindow):
    def __init__(self, config, msg, link=False):
        BaseWindow.__init__(self, config)
        self.msg = msg
        self.link = link
        #For dynamic height
        self.max_height = 100
        self.line_spacing = 0.03
        self.msg_y = self.max_height*self.line_spacing

        if self.title != None and len(self.title)>0:
            self.title_y = self.max_height*(self.line_spacing/2)
            self.msg_y = self.max_height*(self.line_spacing*2)
            self.inc+=2

        self.height = self.max_height

    def _add_title(self):
        if self.title != None and len(self.title)>0:
            self.canvas.create_text(self.width/2, self.title_y, text=self.title, fill=self.msg_color.hex_l, font=self.h1, anchor='n')

    def Prompt(self):
        self._Show()
        self._add_title()
        
        if self.link:
            self._add_link_button(self.msg, self.msg_y+(self.btn_height/2))
        else:
            self.canvas.create_text(self.width/2, self.msg_y, text=self.msg, fill=self.msg_color.hex_l, font=self.h3, anchor='n')

        self.root.mainloop()
        return self


class ChoiceWindow(BaseWindow):
    def __init__(self, config, msg, b_accept, b_decline, entry=False, horizontal=True):
        BaseWindow.__init__(self, config)
        self.msg = msg
        self.b_accept = b_accept
        self.b_decline = b_decline
        self.entry = entry
        self.horizontal = horizontal
        self.num_lines = len(self.msg.split("\n"))
        #For dynamic height
        self.max_height = 900
        self.line_spacing = 0.03
        self.msg_y = self.max_height*self.line_spacing
        self.inc = 1
        self.file_types = config.file_types

        if self.title != None and len(self.title)>0:
            self.title_y = self.max_height*(self.line_spacing/2)
            self.msg_y = self.max_height*(self.line_spacing*2)
            self.inc+=2
        if self.entry:
            self.entry_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
            self.inc+=2
        if self.horizontal:
            self.btn_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
            self.inc+=2
            self.height = (self.max_height+self.btn_height)*(self.line_spacing*(self.num_lines+self.inc))
        if not self.horizontal:
            self.btn_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
            self.inc+=2
            self.btn_y2 = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
            self.inc+=2
            self.height = (self.max_height+self.btn_height)*(self.line_spacing*(self.num_lines+self.inc))

    def Ask(self):
        self._Show()
        self._add_title()
        
        self.canvas.create_text(self.width/2, self.msg_y, text=self.msg, fill=self.msg_color.hex_l, font=self.h3, anchor='n')

        if self.entry:
            self.entry = self.add_entry()
            self.entry.place(x = self.width/2, y = self.entry_y, relwidth = 0.85, anchor='n')

        if self.horizontal:
            self._add_horizontal_buttons(self.b_accept, self.b_decline, self.btn_y)
        else:
            self._add_vertical_buttons(self.b_accept, self.b_decline, self.btn_y, self.btn_y2)
        self.root.mainloop()
        return self

    def Prompt(self):
        self._Show()
        self._add_title()
        
        self.canvas.create_text(self.width/2, self.msg_y, text=self.msg, fill=self.msg_color.hex_l, font=self.h3, anchor='n')
        self._add_single_button(self.b_accept, self.btn_y)
        self.root.mainloop()
        return self

    def DropDown(self, arr):
        self._Show()
        self._add_title()
        
        self.canvas.create_text(self.width/2, self.msg_y, text=self.msg, fill=self.msg_color.hex_l, font=self.h3, anchor='n')

        self.dropdown = self.add_dropdown(arr)
        self.dropdown.place(x = self.width/2, y = self.entry_y, relwidth = 0.65, anchor='n')

        self._add_single_button(self.b_accept, self.btn_y)
        self.root.mainloop()
        return self

    def _add_title(self):
        if self.title != None and len(self.title)>0:
            self.canvas.create_text(self.width/2, self.title_y, text=self.title, fill=self.msg_color.hex_l, font=self.h1, anchor='n')

    def _add_single_button(self, b_accept, y):
        self.b_accept = self.add_choice_btn(b_accept)
        self.b_accept['command'] = self.action_accept
        self.b_accept.place(x = self.width/2-((self.width/2)*0.8), y = y, height = self.btn_height, relwidth = 0.75)

        self.configure_btns()

    def _add_file_select_button(self, b_accept, y):
        self.b_accept = self.add_choice_btn(b_accept)
        self.b_accept['command'] = self.action_file_select
        self.b_accept.place(x = self.width/2-((self.width/2)*0.8), y = y, height = self.btn_height, relwidth = 0.75)

        self.configure_btns()
        
    def _add_vertical_buttons(self, b_accept, b_decline, y, y2):
        self.b_accept = self.add_choice_btn(b_accept)
        self.b_accept['command'] = self.action_accept
        self.b_decline = self.add_choice_btn(b_decline)
        self.b_decline['command'] = self.action_decline
        self.b_accept.place(x = self.width/2-((self.width/2)*0.8), y = y, height = self.btn_height, relwidth = 0.75)
        self.b_decline.place(x = self.width/2-((self.width/2)*0.8), y = y2, height = self.btn_height, relwidth = 0.75)
        self.configure_btns()

    def _add_horizontal_buttons(self, b_accept, b_decline, y):
        self.b_accept = self.add_choice_btn(b_accept)
        self.b_accept['command'] = self.action_accept
        self.b_decline = self.add_choice_btn(b_decline)
        self.b_decline['command'] = self.action_decline
        self.b_accept.place(x = self.padding[0], y = y, height = self.btn_height, relwidth = 0.45, anchor='nw')
        self.b_decline.place(x = (self.width-(self.width*0.45))-self.padding[0], y = y, height = self.btn_height, relwidth = 0.45, anchor='nw')
        self.configure_btns()

    def action_file_select(self, event=None):
        self.root.quit()
        self.response = askopenfilename(filetypes=self.file_types)

        self.root.destroy()

    def action_accept(self, event=None):
        self.root.quit()
        if self.entry != None and self.entry != False:
            if self.dropdown != None and self.dropdown != False:
                self.response = self.dropdown_val.get()
            else:
                self.response = self.entry.get()
        else:
            self.response = self.b_accept.cget('text')
            self.root.quit()

        self.root.destroy()

    def action_decline(self, event=None):
        self.response = self.b_decline.cget('text')
        self.root.quit()
        self.root.destroy()


class FileSelectWindow(ChoiceWindow):
    def __init__(self, config, msg, b_accept, b_decline, entry=False, horizontal=True):
        ChoiceWindow.__init__(self, config, msg, b_accept, b_decline, entry, horizontal)
        self.entry = None
        self.inc = 2

        if self.horizontal:
            self.btn_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
            self.inc+=2
            self.height = (self.max_height+self.btn_height)*(self.line_spacing*(self.num_lines+self.inc))
        if not self.horizontal:
            self.btn_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
            self.inc+=2
            self.btn_y2 = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
            self.inc+=2
            self.height = (self.max_height+self.btn_height)*(self.line_spacing*(self.num_lines+self.inc))

    def FileSelect(self):
        self._Show()
        self._add_title()
        
        self.canvas.create_text(self.width/2, self.msg_y, text=self.msg, fill=self.msg_color.hex_l, font=self.h3, anchor='n')
        self._add_file_select_button(self.b_accept, self.btn_y)
        self.root.mainloop()
        return self


class MultiTextChoiceWindow(ChoiceWindow):
    def __init__(self, config, msg, b_accept, b_decline, entry=True, horizontal=True):
        ChoiceWindow.__init__(self, config, msg, b_accept, b_decline, entry, horizontal)
        if self.entry:
            self.entry_height = self.max_height*(self.line_spacing*4)
            self.inc+=1
        if self.horizontal:
            self.btn_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
            self.inc+=2
            self.height = (self.max_height+self.btn_height)*(self.line_spacing*(self.num_lines+self.inc))
        if not self.horizontal:
            self.btn_y = self.max_height*(self.line_spacing*(self.num_lines+6))
            self.btn_y2 = self.max_height*(self.line_spacing*(self.num_lines+8))
            self.height = (self.max_height+self.btn_height)*(self.line_spacing*(self.num_lines+10))

    def Ask(self):
        self._Show()
        self._add_title()
        self.canvas.create_text(self.width/2, self.msg_y, text=self.msg, fill=self.msg_color.hex_l, font=self.h3, anchor='n')
        self.entry = self.add_entry(True)
        self.entry.place(x = self.width/2-((self.width/2)*0.85), y = self.entry_y, height=self.entry_height, relwidth = 0.85, anchor='nw')

        if self.horizontal:
            self._add_horizontal_buttons(self.b_accept, self.b_decline, self.btn_y)
        else:
            self._add_vertical_buttons(self.b_accept, self.b_decline, self.btn_y, self.btn_y2)

        self.root.mainloop()
        return self

class CopyTextWindow(MultiTextChoiceWindow):
    def __init__(self, config, msg, b_accept, b_decline, entry=True, horizontal=True):
        MultiTextChoiceWindow.__init__(self, config, msg, b_accept, b_decline, entry, horizontal)

    def Ask(self):
        self._Show()
        self._add_title()
        self.canvas.create_text(self.width/2, self.msg_y, text=self.msg, fill=self.msg_color.hex_l, font=self.h3, anchor='n')
        self.entry = self.add_entry(True)
        self.entry.place(x = self.width/2-((self.width/2)*0.95), y = self.entry_y, height=self.entry_height, relwidth = 0.95, anchor='nw')

        if self.horizontal:
            self._add_horizontal_copy_buttons(self.b_accept, self.b_decline, self.btn_y)
        else:
            self._add_vertical_copy_buttons(self.b_accept, self.b_decline, self.btn_y, self.btn_y2)

        self.root.mainloop()
        return self

    def _add_horizontal_copy_buttons(self, b_accept, b_decline, y):
        self.b_accept = self.add_choice_btn(b_accept)
        self.b_accept['command'] = self.action_copy_text
        self.b_decline = self.add_choice_btn(b_decline)
        self.b_decline['command'] = self.action_decline
        self.b_accept.place(x = self.padding[0], y = y, height = self.btn_height, relwidth = 0.45, anchor='nw')
        self.b_decline.place(x = (self.width-(self.width*0.45))-self.padding[0], y = y, height = self.btn_height, relwidth = 0.45, anchor='nw')
        self.configure_btns()

    def _add_vertical_copy_buttons(self, b_accept, b_decline, y, y2):
        self.b_accept = self.add_choice_btn(b_accept)
        self.b_accept['command'] = self.action_copy_text
        self.b_decline = self.add_choice_btn(b_decline)
        self.b_decline['command'] = self.action_decline
        self.b_accept.place(x = self.padding[0], y = y, height = self.btn_height, relwidth = 0.45, anchor='nw')
        self.b_decline.place(x = (self.width-(self.width*0.45))-self.padding[0], y = y2, height = self.btn_height, relwidth = 0.45, anchor='nw')
        self.configure_btns()

    def action_copy_text(self, event=None):
        if self.entry != None:
            txt = self.entry.get('1.0', 'end')
            self.response = tkinter.messagebox.showinfo('Confirm', 'Text copied for 10 seconds')
            thread = threading.Thread(target=self.copy_action, args=[txt])
            thread.setDaemon(True)
            thread.start()

    def copy_action(self, text):
        pyperclip.copy(text)
        time.sleep(10)
        pyperclip.copy("")


class UserPasswordWindow(ChoiceWindow):
    def __init__(self, config, msg, b_accept, b_decline, entry=True, horizontal=True):
        ChoiceWindow.__init__(self, config, msg, b_accept, b_decline, entry, horizontal)
        self.user = None
        self.pw = None
        self.confirm_pw = None
        self.inc-=4
        self.entry_user_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
        self.inc+=2
        self.entry_pw_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
        self.inc+=1
        self.entry_confirm_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
        self.inc+=2
        self.btn_y = self.max_height*(self.line_spacing*(self.num_lines+self.inc))
        self.inc+=2
        self.height = (self.max_height+self.btn_height)*(self.line_spacing*(self.num_lines+self.inc))

    def Ask(self):
        self._Show()
        self._add_title()
        bullet = "\u25CF"
        startx = ((self.width/2)*0.58)
        x = self.width/2-startx
        x_shft_lable = 1.25
        x_shft_entry = 1.35

        self.canvas.create_text(self.width/2, self.msg_y, text=self.msg, fill=self.msg_color.hex_l, font=self.h3, anchor='n')
        self.canvas.create_text(x*x_shft_lable, self.entry_user_y, text='  USER  ', fill=self.msg_color.hex_l, font=self.font, anchor='ne')
        self.canvas.create_text(x*x_shft_lable, self.entry_pw_y, text='PASSWORD', fill=self.msg_color.hex_l, font=self.font, anchor='ne')
        self.canvas.create_text(x*x_shft_lable, self.entry_confirm_y, text='CONFIRM ', fill=self.msg_color.hex_l, font=self.font, anchor='ne')
        self.user = self.add_entry()
        self.user.place(x = x*x_shft_entry, y = self.entry_user_y, relwidth = 0.6)
        self.pw = self.add_entry()
        self.pw['show'] = bullet
        self.pw.place(x = x*x_shft_entry, y = self.entry_pw_y, relwidth = 0.6)
        self.confirm_pw = self.add_entry()
        self.confirm_pw['show'] = bullet
        self.confirm_pw.place(x = x*x_shft_entry, y = self.entry_confirm_y, relwidth = 0.6)

        self._add_login_button(self.b_accept, self.btn_y)

        self.root.mainloop()
        return self

    def _add_login_button(self, b_accept, y):
        self.b_accept = self.add_choice_btn(b_accept)
        self.b_accept['command'] = self.action_login
        self.b_accept.place(x = self.width/2-((self.width/2)*0.8), y = y, height = self.btn_height, relwidth = 0.75)

        self.configure_btns()

    def action_login(self, event=None):
        self.root.quit()
        if self.user != None and self.pw != None and self.confirm_pw != None:
            user = self.user.get()
            pw = self.pw.get()
            confirm = self.confirm_pw.get()
            if len(user)>0 and len(pw)>0 and len(confirm):
                if pw == confirm:
                    self.response = {'user':user, 'pw':pw}
                    self.root.destroy()
                else:
                    self.response = tkinter.messagebox.showerror('ERROR', 'Passwords are different.')
            else:
                self.response = tkinter.messagebox.showerror('ERROR', 'All fields must be filled')

        else:
            self.response = self.b_accept.cget('text')
            self.root.quit()
