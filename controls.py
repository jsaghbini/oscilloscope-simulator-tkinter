# -*- coding: utf-8 -*-
from email import message
import tkinter as tk
import json
import time
import os
from turtle import color
from observer import Subject, Observer
from screen import Screen
from generator import Generator
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from tkinter.filedialog import asksaveasfile

# ╔════════════════════════════════════════════════════╤═══════════════════════╗
# ║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│    Signal Controls    ║
# ╚════════════════════════════════════════════════════╧═══════════════════════╝
class SignalControls(tk.LabelFrame, Subject, Observer):
    def __init__(self, parent, model, *args, **kwargs):
        Subject.__init__(self)
        super().__init__(parent, *args, text=model.get_name(), **kwargs)
        self.parent = parent
        self.model = model
        self.create_controls()
        model.attach(self)
        self.update(model)

    def __repr__(self):
        return "SignalControls()"

    def get_generator(self):
        return self.model

    def set_generator(self, generator):
        self.model.detach(self)
        self.model = generator
        generator.attach(self)
        self.update(generator)

    def create_controls(self):
        harmonics_frame = tk.LabelFrame(self, name="harmonicsFrame", text="Harmonics")
        self.harmo_odd_even_var = tk.IntVar()
        btn = tk.Radiobutton(
            harmonics_frame,
            name="harmonicsAllRadioButton",
            text="All",
            variable=self.harmo_odd_even_var,
            value=1,
            command=self.cb_change
        )
        btn.select()
        btn.pack(side="left")
        btn = tk.Radiobutton(
            harmonics_frame,
            name="harmonicsOddRadioButton",
            text="Odd",
            variable=self.harmo_odd_even_var,
            value=2,
            command=self.cb_change
        )
        btn.pack(side="left")
        harmonics_frame.pack()

        self.mag_var = tk.DoubleVar()
        self.scale_mag = tk.Scale(
            self,
            name="amplitudeScale",
            variable=self.mag_var,
            label="Amplitude",
            orient="horizontal",
            length=250,
            from_=0,
            to=1,
            relief="raised",
            sliderlength=20,
            resolution=0.1,
            tickinterval=0.5,
            command=self.cb_change
        )
        self.scale_mag.pack()
        self.freq_var = tk.IntVar()
        self.scale_freq = tk.Scale(
            self,
            name="frequencyScale",
            variable=self.freq_var,
            label="Frequency",
            orient="horizontal",
            length=250,
            from_=1,
            to=50,
            relief="raised",
            sliderlength=20,
            tickinterval=5,
            command=self.cb_change
        )
        self.scale_freq.pack()
        self.phase_var = tk.IntVar()
        self.scale_phase = tk.Scale(
            self,
            name="phaseScale",
            variable=self.phase_var,
            label="Phase",
            orient="horizontal",
            length=250,
            from_=-90,
            to=90,
            relief="raised",
            sliderlength=20,
            tickinterval=20,
            command=self.cb_change
        )
        self.scale_phase.pack()
        self.harmonics_var = tk.IntVar()
        self.scale_harmonics = tk.Scale(
            self,
            name="harmonicsScale",
            variable=self.harmonics_var,
            label="Harmonics",
            orient="horizontal",
            length=250,
            from_=1,
            to=50,
            relief="raised",
            sliderlength=20,
            tickinterval=5,
            command=self.cb_change
        )
        self.scale_harmonics.pack()
        self.samples_var = tk.IntVar()
        self.scale_samples = tk.Scale(
            self,
            name="samplesScale",
            variable=self.samples_var,
            label="Samples",
            orient="horizontal",
            length=250,
            from_=10,
            to=500,
            relief="raised",
            sliderlength=20,
            tickinterval=70,
            command=self.cb_change
        )
        self.scale_samples.pack()

    def update(self, generator):
        self.config(text=generator.get_name())
        self.harmo_odd_even_var.set(generator.harmo_odd_even)
        self.mag_var.set(generator.get_magnitude())
        self.freq_var.set(generator.get_frequency())
        self.phase_var.set(generator.get_phase())
        self.harmonics_var.set(generator.get_harmonics())
        self.samples_var.set(generator.get_samples())

    def cb_change(self, event=None):
        self.notify()                                                                                      
        
# ╭────────────────────╮
# │ End Signal Controls├───────────────────────────────────────────────────────────────────
# ╰────────────────────╯

class Controller(Observer, Subject):
    def __init__(self, parent, screen, models):
        self.parent = parent
        self.screen = screen
        self.models = models
        self.parameters_frames = []
        for model in models:
            self.screen.add_generator(model)
            parameters_frame = SignalControls(parent, model, name=f'_{model.get_name()}Frame')
            self.parameters_frames.append(parameters_frame)
            parameters_frame.attach(self)
        self.create_controls()

# ╔════════════════════════════════════════════════════╤═══════════════════════╗
# ║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│        Menu Bar       ║
# ╚════════════════════════════════════════════════════╧═══════════════════════╝
        menu = tk.Menu(parent)
        parent.config(menu=menu)

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Open",command=self.open)
        fileMenu.add_command(label="Save JSON",command=self.save)
        fileMenu.add_command(label="Save Image",command=self.save_img)
        #fileMenu.add_command(label="Exit Instantly", command=self.close_app)
        fileMenu.add_command(label="Exit", command=self.close_app_ask)
        menu.add_cascade(label="File", menu=fileMenu)

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="About Us ...",command=self.about_us)
        fileMenu.add_command(label="About Tk ...",command=self.about_tk)
        fileMenu.add_command(label="About Python ...",command=self.about_py)
        fileMenu.add_command(label="About our Application ...",command=self.about_app)
        menu.add_cascade(label="Help", menu=fileMenu)

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Background",command=self.color_bg)
        fileMenu.add_command(label="Curves",command=self.color_curves)
        # fileMenu.add_command(label="Scales",command=self.color_scales)
        # fileMenu.add_command(label="Check-Boxes",command=self.color_checkboxes)
        menu.add_cascade(label="Color Picker", menu=fileMenu)


    def open(self):
        file = filedialog.askopenfilename()
        filename = os.path.basename(file)
        res = messagebox.askyesno("J&H Oscilloscope", 'Are you sure you want to load "' +filename + ' " ?') 
        if res == True:
            with open(file) as f:
                data = json.load(f)
                if 'X'  not in data or 'Y' not in data:
                    messagebox.showerror('error', "This json file doesn't contain X and/or Y data.")
                    f.close()
                    return
                for model in self.models:    
                    phaseSave = data[model.get_name()]['phase']
                    ampliSave = data[model.get_name()]['amplitude']
                    freqSave = data[model.get_name()]['frequency']
                    harmSave = data[model.get_name()]['harmonics']
                    model.set_phase(phaseSave)
                    model.set_magnitude(ampliSave)
                    model.set_frequency(freqSave)
                    model.set_harmonics(harmSave)

                    parameters_frame = SignalControls(self.parent, model, name=f'_{model.get_name()}Frame')
                    self.parameters_frames.append(parameters_frame)
                    parameters_frame.attach(self)
                    self.update(parameters_frame)
                self.create_controls()
                f.close()

        elif res == False:
            pass
        else:
            messagebox.showerror('error', 'something went wrong!')
        
    def save(self):
        data = {}
        for model in self.models:
            phaseSave = model.get_phase()
            ampliSave = model.get_magnitude()
            freqSave = model.get_frequency()
            harmSave = model.get_harmonics()
            data[model.get_name()] = {}
            data[model.get_name()]['phase'] = phaseSave
            data[model.get_name()]['amplitude'] = ampliSave
            data[model.get_name()]['frequency'] = freqSave
            data[model.get_name()]['harmonics'] = harmSave
        
        files = [('JSON File', '*.json')]
        filepos = asksaveasfile(filetypes = files,title="Save...",defaultextension = json,initialfile='params.json')
        json.dump(data, filepos)
        messagebox.showinfo("J&H Oscilloscope","Your file has been saved!")

    def save_img(self):  
        formats = [('Portable Network Graphics','*.png')]
        filename = filedialog.asksaveasfilename(filetypes=formats,title="Save...",initialfile='graphe')
        time.sleep(0.2) # To make sure the "menu" is closed and does not appear in the screenshot
        self.screen.save_as_png(self.screen.canvas,filename)
        messagebox.showinfo("J&H Oscilloscope","Your image has been saved!")

    def close_app(self):
        exit()

    def close_app_ask(self):
        res = messagebox.askyesno("J&H Oscilloscope", 'Do you want to exit?') 
        if res == True:
            exit()

        elif res == False:
            pass
        else:
            messagebox.showerror('error', 'something went wrong!')

    def about_us(self):
         messagebox.showinfo('About Us', "=->> Project Creators <<-=\nJohnny Saghbini & Hassan Serhan\n\n\nAll Rights Reserved © 2022")

    def about_tk(self):
        messagebox.showinfo('About TkInter', "Tkinter 'Tool Kit Interface' est la bibliothèque graphique libre d'origine pour le langage Python, permettant la création d'interfaces graphiques. Elle vient d'une adaptation de la bibliothèque graphique Tk écrite pour Tcl. ")
    
    def about_py(self):
        messagebox.showinfo('About Python', "Python est un langage de programmation interprété, multi-paradigme et multiplateformes. Il favorise la programmation impérative structurée, fonctionnelle et orientée objet. Il est doté d'un typage dynamique fort, d'une gestion automatique de la mémoire par ramasse-miettes et d'un système de gestion d'exceptions.Le langage Python fonctionne sur la plupart des plates-formes informatiques, des smartphones aux ordinateurs centraux5, de Windows à Unix avec notamment GNU/Linux en passant par macOS, ou encore Android, iOS, et peut aussi être traduit en Java ou .NET. Il est conçu pour optimiser la productivité des programmeurs en offrant des outils de haut niveau et une syntaxe simple à utiliser. ")

    def about_app(self):
        messagebox.showinfo("About our Application","Pour lancer ce programme et eviter les erreurs, veuillez installer les deux libraries WebColors et SciPy en utilisant les commandes suivantes:\n1. pip install webcolors\n2. pip install scipy")

    def color_bg(self):
       # curves = colorchooser.askcolor(title ="Choose a color for your curves")
        #SignalControls.scale_harmonics.config(fg=curves[1])
        self.screen.color_of_background()
        #color_me.config(fg=curves[1])

    def color_curves(self):
       # curves = colorchooser.askcolor(title ="Choose a color for your curves")
        #SignalControls.scale_harmonics.config(fg=curves[1])
        self.screen.color_of_curves()
        #color_me.config(fg=curves[1])

    def color_scales(self):
        scales = colorchooser.askcolor(title ="Choose a color for your scales")
        tk.Scale.colo

    def color_checkboxes(self):
        checkboxes = colorchooser.askcolor(title ="Choose a color for your checkboxes")
        #color_me.config(fg=checkboxes[1])
# ╭──────────────╮
# │ End Menu Bar ├───────────────────────────────────────────────────────────────────
# ╰──────────────╯

    def __repr__(self):
        return "Controller()"

    def create_controls(self):
        xy_frame = tk.LabelFrame(self.parent, name="xyFrame", text="X-Y")
        self.x_check_var = tk.IntVar()
        btn = tk.Checkbutton(
            xy_frame,
            name="xCheckButton",
            text="X",
            variable=self.x_check_var,
            command=self.cb_x_change
        )
        btn.select()
        btn.pack(side="left")
        self.y_check_var = tk.IntVar()
        btn = tk.Checkbutton(
            xy_frame,
            name="yCheckButton",
            text="Y",
            variable=self.y_check_var,
            command=self.cb_y_change
        )
        btn.select()
        btn.pack(side="left")

        xy_frame.pack()
        self.screen.canvas.pack(expand=1,fill="both",padx=6)
        for parameters_frame in self.parameters_frames:
            parameters_frame.pack(side="left")

    def update(self, parameters_frame):
        generator = parameters_frame.get_generator()
        generator.set_magnitude(parameters_frame.mag_var.get())
        generator.set_frequency(parameters_frame.freq_var.get())
        generator.set_phase(parameters_frame.phase_var.get())
        generator.set_harmonics(parameters_frame.harmonics_var.get())
        generator.set_samples(parameters_frame.samples_var.get())
        generator.harmo_odd_even = parameters_frame.harmo_odd_even_var.get()
        generator.generate()

    def cb_x_change(self):
        generator = None
        for gen in self.models:
            if gen.get_name() == 'X':
                generator = gen
                break

        if generator is None:
            return
        
        if self.x_check_var.get():
            self.screen.add_generator(generator)
        else:
            self.screen.remove_generator(generator)

    def cb_y_change(self):
        generator = None
        for gen in self.models:
            if gen.get_name() == 'Y':
                generator = gen
                break

        if generator is None:
            return
        
        if self.y_check_var.get():
            self.screen.add_generator(generator)
        else:
            self.screen.remove_generator(generator)
