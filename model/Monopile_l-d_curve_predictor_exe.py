#!/usr/bin/env python
# coding: utf-8

# In[64]:


import pandas as pd
import numpy as np
import os
import tkinter as tk
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.svm import SVR
from joblib import dump, load
from tkinter import filedialog

executable_dir = sys._MEIPASS
#
path_model = os.path.join(executable_dir, "svr_monopile_wholecurve.joblib")
path_scaler = os.path.join(executable_dir, "svr_scaling_monopile_wholecurve.joblib")
#
svr_surrogate = load(path_model)
scaler        = load(path_scaler)
#

#
def generate_plot():
    
    # Clear any previous error message
    error_label.config(text="")
    dt_label.config(text="")
    ld_label.config(text="")
    result_label.config(text="")
    plt.clf()
        
    Dia_m = float(Dia_m_entry.get())
    Thickness_m = float(Thickness_m_entry.get())
    Embedded_Length_m = float(Embedded_Length_m_entry.get())
    Dt_ratio = Dia_m / Thickness_m
    LD_ratio = Embedded_Length_m / Dia_m

    if (30 <= Dt_ratio <= 100) and (3 <= LD_ratio <= 10) and (0.5 <= Dia_m <= 2.5) :
        
        dt_label.config(text=f"Dt_ratio: {Dt_ratio:.2f}")
        ld_label.config(text=f"LD_ratio: {LD_ratio:.2f}")
        
        xinp = []
        xtemp = []
        
        for i in range(0,20):
            if i < 5:
                disp =  (Dia_m*1000*0.15/100)*i/4    
                xtemp = [Dia_m, Thickness_m, Embedded_Length_m, disp]
                xinp.append(xtemp)
            else:
                disp =  (Dia_m*1000*0.15 - Dia_m*1000*0.15/100)*(i-4)/15 + Dia_m*1000*0.15/100  
                xtemp = [Dia_m, Thickness_m, Embedded_Length_m, disp]
                xinp.append(xtemp)

        xinp_df = pd.DataFrame(xinp, columns=["Dia_m", "Thickness_m", "Embedded length_m", "Ux_mm"])

        #
        xinp_scaled = scaler.transform(xinp)
        #
        prediction_vec = svr_surrogate.predict(xinp_scaled)
        #
        results = xinp_df.copy()
        #
        results['Fx_kN'] = prediction_vec      
        
        plt.plot(results['Ux_mm'],results['Fx_kN'], color = 'black')
        plt.title(f"Monopile Load-Displacement Curve")
        plt.xlabel('Displacement (mm)')
        plt.ylabel('Load (kN)')
        plt.show(block=False)   
        
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            results.to_csv(save_path, index=False)
            result_label.config(text=f"Results saved to {save_path}")
            result_label.update()
    else:
        error_label.config(text="Pile geometry out of the training range. Please Change input values within Diameter_m[0.5, 2.5], Dt_ratio[30,100], LD_ratio[3,10]")

        
app = tk.Tk()
app.title("Offshore Monopile Load-Displacement Curve Predictor")
app.geometry("1000x800")

Dia_m_label = tk.Label(app, text="Diameter (m):")
Dia_m_label.pack()
Dia_m_entry = tk.Entry(app)
Dia_m_entry.pack()

Thickness_m_label = tk.Label(app, text="Thickness (m):")
Thickness_m_label.pack()
Thickness_m_entry = tk.Entry(app)
Thickness_m_entry.pack()

Embedded_Length_m_label = tk.Label(app, text="Embedded Length (m):")
Embedded_Length_m_label.pack()
Embedded_Length_m_entry = tk.Entry(app)
Embedded_Length_m_entry.pack()

generate_button = tk.Button(app, text="Calculate", command=generate_plot)
generate_button.pack()

error_label = tk.Label(app, text="", fg="red")
error_label.pack()

dt_label = tk.Label(app, text="", fg="green")
dt_label.pack()

ld_label = tk.Label(app, text="", fg="green")
ld_label.pack()

result_label = tk.Label(app, text="", fg="blue")
result_label.pack()

app.mainloop()



# In[ ]:




