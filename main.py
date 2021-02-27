import tkinter as tk
import numpy as np
import pygubu
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from scipy import interpolate
import os
import sys

try:
    DATA_DIR = os.path.abspath(os.path.dirname(__file__))
except NameError:
    DATA_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

UI_FILE = os.path.join(DATA_DIR, "interface.ui")
ICON_FILE = os.path.join(DATA_DIR, 'imgs', 'hhh1.png')

class Application:
    def __init__(self,master):
        self.master=master
        self.builder=builder=pygubu.Builder()
        builder.add_from_file(UI_FILE)
        self.mainwindow=builder.get_object('main_frame',master)
        self.text=builder.get_object('text_1')
        self.browse = builder.get_object('btn_browse')
        self.seq_bin=""
        self.V_sortie=[]
        self.abscisse=[]
        self.msg_err=""
        self.longueur=0
        self.c1 = Figure()
        self.c2 = Figure()
        self.cb_Volt = builder.get_object('cb_Volt')
        self.cb_Res = builder.get_object('cb_Res')
        self.V_ref=10
        self.R=5
        self.top3=tk.Toplevel



        self.canvas1=canvas1=builder.get_object('canvas_1')
        self.canvas2 = canvas2 = builder.get_object('canvas_2')

        # Setup matplotlib canvas
        self.figure1 = fig1 = Figure(figsize=(4, 2), dpi=100)
        self.can1 = can1 = FigureCanvasTkAgg(fig1, master=canvas1)
        can1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Setup matplotlib toolbar (optional)
        self.toolbar1 = NavigationToolbar2Tk(can1, canvas1)
        self.toolbar1.update()
        can1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Setup matplotlib canvas2
        self.figure = fig = Figure(figsize=(4, 1.5), dpi=100)
        self.canvas = canvas = FigureCanvasTkAgg(fig, master=canvas2)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Setup matplotlib toolbar (optional) 2
        self.toolbar = NavigationToolbar2Tk(canvas, canvas2)
        self.toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.reset()
        self.cb_Volt.current(0)
        self.cb_Res.current(0)




        builder.connect_callbacks(self)

    def about_window(self):
        frame3=tk.Frame
        try:
            self.quit_about()
        except:
            ""
        builder2 = pygubu.Builder()
        builder2.add_from_file('interface.ui')
        self.top3 = tk.Toplevel(self.mainwindow)
        frame3 = builder2.get_object('frame_abt',self.top3)
        img_label=builder2.get_object("label_img")
        img_label.new_image = tk.PhotoImage(file="imgs/hhh1.png")
        img_label.config(image=img_label.new_image)
        self.top3.iconphoto(True, self.icon)
        callbacks = {}
        builder2.connect_callbacks(self)

    def quit_about(self):
        self.top3.destroy()


    def reset(self):
        self.can1.get_tk_widget().forget()
        self.canvas.get_tk_widget().forget()
        self.toolbar1.forget()
        self.toolbar.forget()
        self.canvas1 = canvas1 = self.builder.get_object('canvas_1')
        self.canvas2 = canvas2 = self.builder.get_object('canvas_2')

        # Setup matplotlib canvas
        self.figure1 = fig1 = Figure(figsize=(5, 2), dpi=100)
        self.can1 = can1 = FigureCanvasTkAgg(fig1, master=canvas1)
        can1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar1 = NavigationToolbar2Tk(can1, canvas1)
        self.toolbar1.update()

        # Setup matplotlib canvas2
        self.figure = fig = Figure(figsize=(5, 2), dpi=100)
        self.canvas = canvas = FigureCanvasTkAgg(fig, master=canvas2)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(canvas, canvas2)
        self.toolbar.update()

        self.figure.subplots_adjust(top=0.886, right=0.976, bottom=0.22, left=0.129)
        self.figure1.subplots_adjust(top=0.886, right=0.976, bottom=0.22, left=0.129)


        self.c1 = self.figure.add_subplot(111)
        self.c2 = self.figure1.add_subplot(111)

        self.c1.set_ylabel("Tension (V)")
        self.c1.set_xlabel("Instant t")
        self.c1.set_title("Représentation du signal Analogique")

        self.c2.set_ylabel("Symbole binaire")
        self.c2.set_xlabel("Instant t")
        self.c2.set_title("Représentation du signal Numérique")
        #self.V_sortie=[]

        #self.can1.draw()

    def plot(self):
        try:
            verified=self.cna()
            if verified:
                #######courbe binaire
                bin = [int(self.seq_bin[i]) for i in range(self.longueur)]
                x_bin = [i for i in range(0, self.longueur * 10, 10)]
                self.c2.step(x_bin, bin)

                ########courbe analogique
                x_new = np.linspace(1, int(self.longueur / 4), 300)
                a_BSpline = interpolate.make_interp_spline(self.abscisse, self.V_sortie)
                V_s = a_BSpline(x_new)
                self.c1.plot(x_new, V_s)

                self.canvas.draw()
                self.can1.draw()
            else:
                #rise error
                print("error"+str(verified)+str())
                self.rise_err()
        except Exception as e:
            tk.messagebox.showerror(title="Erreur", message="Erreur inconnue, L'application va se fermer \n" + str(e))
            self.btn_exit()

    def rise_err(self):
        tk.messagebox.showerror(title="Erreur", message=self.msg_err)

    def get_V_R(self):
        v_mv=str(self.builder.get_object("cb_Volt").get())
        r_mr=str(self.builder.get_object("cb_Res").get())
        tmpV=self.builder.get_object("tb_Volt").get()
        tmpR=self.builder.get_object("tb_Res").get()
        tmpV=tmpV.rstrip("\n")
        tmpV=tmpV.replace(",",".")
        tmpR=tmpR.rstrip("\n")
        tmpR = tmpR.replace(",", ".")
        try:
            if v_mv=="V":
                self.V_ref = float(tmpV)
            else:
                self.V_ref = float(tmpV)*0.001
            if r_mr=="Ω":
                self.R = float(tmpR)
            else:
                self.R = float(tmpR)*0.001
        except:
            tk.messagebox.showerror(title="Erreur", message="Erreur d'entrée dans les champs V_ref et R")
            self.V_ref = 10
            self.R = 5


    def cna(self):
        self.seq_bin = self.text.get("1.0",tk.END)
        self.seq_bin = self.seq_bin.rstrip("\n")
        verified = self.verif_seq_bin()
        if verified:
            self.longueur = len(self.seq_bin)
            print(self.longueur)
            self.abscisse = [i + 1 for i in range(0, int(len(self.seq_bin) / 2), 2)]
            self.V_sortie = []
            #self.V_ref =V_ref= 10  # 10V
            #self.R = R = 5  # 5 ohm
            V_ref=self.V_ref
            R=self.R
            print(str(V_ref)+" "+str(R))
            for k in range(int(self.longueur / 4)):
                indice = k * 4
                i3 = (V_ref * int(self.seq_bin[indice])) / (4 * R)
                i2 = (V_ref * int(self.seq_bin[indice + 1])) / (8 * R)
                i1 = (V_ref * int(self.seq_bin[indice + 2])) / (16 * R)
                i0 = (V_ref * int(self.seq_bin[indice + 3])) / (32 * R)
                self.V_sortie.append(2 * R * (i3 + i2 + i1 + i0))

        return verified

    def browse_nd_read(self):
        file = tk.filedialog.askopenfile(mode="r",filetypes=[('', '.txt')])
        if (file is not None):
            print(type(file))
            self.seqbin = file.read()
            self.text.config(state=tk.NORMAL)
            self.text.delete(1.0, tk.END)
            self.text.insert("end", self.seqbin)
            self.text.config(state=tk.DISABLED)
    def verif_seq_bin(self):
        verified=True
        self.msg_err = ""
        if len(self.seq_bin)<16:
            verified=False
            print("<16 : " + str(len(self.seq_bin)))
            self.msg_err="Longueur de la sequence binaire est inferieur à 16 ("+str(len(self.seq_bin))+") "
        #if not self.seq_bin.isnumeric():
         #   verified=False
        #else:
        else:
            for x in self.seq_bin:
                if x not in {'0','1'}:
                    verified=False
                    print("not 0 or 1") #debugging
                    self.msg_err="La sequence contient des valeurs autres que 0 et 1"
                    break
        if verified:
            if len(self.seq_bin)%4 != 0:
                print(str(len(self.seq_bin)%4))
                for i in range(4-(len(self.seq_bin)%4)):
                    self.seq_bin=self.seq_bin+"0"
                    print(self.seq_bin)

        return verified

    def browse_enabler(self,radio):
        if (radio=="rad_browse") :
            self.text.delete(1.0, tk.END)
            self.text.config(state=tk.DISABLED)
            self.browse.config(state=tk.NORMAL)
        else:
            self.text.config(state=tk.NORMAL)
            self.text.delete(1.0, tk.END)
            self.browse.config(state=tk.DISABLED)

    def btn_exit(self):
        #self.can1.get_tk_widget().forget()
        #self.canvas.get_tk_widget().forget()
        self.master.quit()


if __name__ == '__main__' :
    root=tk.Tk()
    app=Application(root)
    app.icon = tk.PhotoImage(file=ICON_FILE)
    root.iconphoto(True, app.icon)
    root.title("Convertisseur Numerique Analogique R-2R")
    root.mainloop()