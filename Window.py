from tkinter import *
import TransferFunction
import Ifstatement
import Signals
#import PlotDraw
import numpy as np
import math
import string

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as pt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

WINDOW_HEIGHT = 300
WINDOW_WIDTH = 300





class Interface:
    STEP = 0
    b0 = "b0"
    a0 = "a0"
    a1 = "a1"
    a2 = "a2"
    a3 = "a3"
    i = 0

    X = []
    Y = []

    signal_choose = 69

    def createString(self):
        string = "s^4 + " + str(self.a3)
        string += "*s^3 + " + str(self.a2)
        string += "*s^2 + " + str(self.a1)
        string += "*s^1 + " + str(self.a0)
        return string

    def __init__(self):
        self.root = Tk()

        self.plot = Canvas(master=self.root).grid(row=8, column=3)

        self.b0_label = Label(master=self.root, text="b0: ").grid(row=0, column=0)
        self.b0_input = Entry(master=self.root)
        self.b0_input.grid(row=0, column=1)
        self.a0_label = Label(master=self.root, text="a0: ").grid(row=1, column=0)
        self.a0_input = Entry(master=self.root)
        self.a0_input.grid(row=1, column=1)
        self.a1_label = Label(master=self.root, text="a1: ").grid(row=2, column=0)
        self.a1_input = Entry(master=self.root)
        self.a1_input.grid(row=2, column=1)
        self.a2_label = Label(master=self.root, text="a2: ").grid(row=3, column=0)
        self.a2_input = Entry(master=self.root)
        self.a2_input.grid(row=3, column=1)
        self.a3_label = Label(master=self.root, text="a3: ").grid(row=4, column=0)
        self.a3_input = Entry(master=self.root)
        self.a3_input.grid(row=4, column=1)

        self.sinus = Radiobutton(master=self.root, text="Sinus signal", variable=self.signal_choose, value=1, command=self.setsine).grid(row=5, column=0)
        self.recktangle = Radiobutton(master=self.root, text="Recktangle signal", variable=self.signal_choose, value=1, command=self.setrec).grid(row=6, column=0)
        self.triangle = Radiobutton(master=self.root, text="Triangle signal", variable=self.signal_choose, value=3, command=self.settri).grid(row=7, column=0)

        self.start_button = Button(master=self.root, text="Start", command=self.start).grid(row=8, column=0)

        self.Routh_stability_check = Label(master=self.root, bg="yellow", width=3, height=1, text="R").grid(row=1, column=3)
        self.Hurwitz_stability_check = Label(master=self.root, bg="green", width=3, height=1, text="R-H").grid(row=3, column=3)

        self.tf_denominator_label = Label(master=self.root, text=self.b0).grid(row=1, column=2)
        self.tf_label = Label(master=self.root, text="----------------------------------------").grid(row=2, column=2)
        self.tf_numerator_label = Label(master=self.root, text=self.createString()).grid(row=3, column=2)

        self.amplification_input = Entry(master=self.root)
        self.amplification_input.grid(row=5, column=1)
        self.length_input = Entry(master=self.root)
        self.length_input.grid(row=6, column=1)
        self.period_input = Entry(master=self.root)
        self.period_input.grid(row=7, column=1)



    def start(self):
        try:
            self.b0 = float(self.b0_input.get())
            self.a0 = float(self.a0_input.get())
            self.a1 = float(self.a1_input.get())
            self.a2 = float(self.a2_input.get())
            self.a3 = float(self.a3_input.get())
        except ValueError:
            print("Input must be a number")
            return 0
        self.tf_denominator_label = Label(master=self.root, text="                                                                   ").grid(row=1, column=2)
        self.tf_numerator_label = Label(master=self.root, text="                                                                    ").grid(row=3, column=2)                          #REFRESSSHHHHHHHHH
        self.tf_denominator_label = Label(master=self.root, text=self.b0).grid(row=1, column=2)
        self.tf_numerator_label = Label(master=self.root, text=self.createString()).grid(row=3, column=2)

        parameters = TransferFunction.TransferFunction.read_dictionary(self.b0, self.a0, self.a1, self.a2, self.a3)
        is_routh_stable = Ifstatement.Ifstatement.routh_stability_check(parameters)
        stateVariable = {"x1": 0, "x2": 0, "x3": 0, "x4": 0}

        X = []
        Y = []
        SIG = []

        for x in range(0, 200):
            Y.append(stateVariable["x1"])
            X.append(self.STEP)
            for y in range(0, 500):
                dx4 = (-(self.a0*stateVariable["x1"])-(self.a1*stateVariable["x2"])-(self.a2*stateVariable["x3"])-(self.a3*stateVariable["x4"]) + float(self.signal()))*TransferFunction.integralStep
                stateVariable["x4"] += dx4
                dx3 = stateVariable["x4"]*TransferFunction.integralStep
                stateVariable["x3"] += dx3
                dx2 = stateVariable["x3"]*TransferFunction.integralStep
                stateVariable["x2"] += dx2
                dx1 = stateVariable["x2"]*TransferFunction.integralStep
                stateVariable["x1"] += dx1
                self.STEP += TransferFunction.integralStep
            SIG.append(self.signal())

        Interface.plot(self,X,SIG)

        self.what_a_button = Button(master=self.root, text="Change", command=self.plot2).grid(row=8, column=1)



        if is_routh_stable:
            self.Routh_stability_check = Label(master=self.root, bg="green", width=3, height=1, text="R").grid(row=1, column=3)
        else:
            self.Routh_stability_check = Label(master=self.root, bg="red", width=3, height=1, text="R").grid(row=1, column=3)

        is_hurwitz_stable = Ifstatement.Ifstatement.hurwitz_stability_check(parameters)

        if is_hurwitz_stable == 1:
            self.Hurwitz_stability_check = Label(master=self.root, bg="green", width=3, height=1, text="R-H").grid(row=3, column=3)
        elif is_hurwitz_stable == 0:
            self.Hurwitz_stability_check = Label(master=self.root, bg="yellow", width=3, height=1, text="R-H").grid(row=3, column=3)
        else:
            self.Hurwitz_stability_check = Label(master=self.root, bg="red", width=3, height=1, text="R-H").grid(row=3, column=3)

    def mainwindow(self):
        self.root.title('Title')
        self.root.config(bg="white", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.root.mainloop()

    def plot(self, X, Y):

        fig = Figure(figsize=(6, 4))
        a = fig.add_subplot(111)
        a.plot(X, Y, color='black')

        a.set_title("Estimation Grid", fontsize=13)
        a.set_ylabel("Y", fontsize=11)
        a.set_xlabel("X", fontsize=11)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().grid(row=8, column=3)
        canvas.draw()

    def test(self):
        Interface.plot2(self, self.X, self.Y)

    def plot2(self):
        f = np.logspace(-1, 6, float(1e3))
        w = 2 * np.pi * f
        coeff = [1,self.a3, self.a2, self.a1, self.a0]
        np.roots(coeff)
        Y0 = 1
        Y1 = 1j * w - np.roots(coeff)[0]
        Y2 = 1j * w - np.roots(coeff)[1]
        Y3 = 1j * w - np.roots(coeff)[2]
        Y4 = 1j * w - np.roots(coeff)[3]
        H = Y0 / (Y1 * Y2 * Y3 * Y4)

        fig = Figure(figsize=(6, 4))
        fig1 = Figure(figsize=(6, 4))
        a = fig.add_subplot(111)
        a1 = fig1.add_subplot(111)
        a.plot(self.Y ,self.X, color='black')

        a.set_title("Magnitude", fontsize=13)
        a.set_ylabel("Y", fontsize=11)
        a.set_xlabel("X", fontsize=11)
        a.semilogx(f, 20 * np.log10(abs(H)))
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().grid(row=8, column=3)
        canvas.draw()

        a1.set_title("Phase", fontsize=13)
        a1.set_ylabel("Y", fontsize=11)
        a1.set_xlabel("X", fontsize=11)
        a1.semilogx(f,np.angle(H)*180/np.pi)
        canvas2 = FigureCanvasTkAgg(fig1, master=self.root)
        canvas2.get_tk_widget().grid(row=8, column=4)
        canvas2.draw()

    def signal(self):
        _amp = float(self.amplification_input.get())
        qz = float(self.period_input.get())
        _per = qz*TransferFunction.integralStep
        if self.signal_choose == 1:
            return float(_amp*math.sin(self.STEP))+float(_amp)
        if self.signal_choose == 2:
            period = str((self.STEP / 6.28)%6.28)
            if int(period[0]) % 2 == 0:
                return float(2*_amp)
            else:
                return float(0)
        if self.signal_choose == 3:
            period = str((self.STEP % 4)/4)
            if int(period[0]) % 4 == 0 or int(period[0]) % 4 == 3:
                self.i += TransferFunction.integralStep
            else:
                self.i -= TransferFunction.integralStep
            return float(self.i*_amp/4)

        if self.signal_choose == 69:
            return float(_amp)

    def setsine(self):
        self.signal_choose = 1
        print("sin")
        return 0
    def setrec(self):
        print("rec")
        self.signal_choose = 2
        return 0
    def settri(self):
        self.signal_choose = 3
        return 0



