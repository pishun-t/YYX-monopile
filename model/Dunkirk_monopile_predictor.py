import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.svm import SVR
from joblib import dump, load


path_main = "D:\\Users\\dmgta\\OneDrive - Imperial College London\\Documents\\Github\\Surrogates\\2023 Dunkirk monopile\\SVM\\" # change the location of the file
#
path_out    = path_main+ "predictions_wholecurve.csv"
path_model  = path_main+ "svr_monopile_wholecurve.joblib"
path_scaler = path_main+ "svr_scaling_monopile_wholecurve.joblib"
#
print('*** loading model')
svr_surrogate = load(path_model)
scaler        = load(path_scaler)
#
print('*** making a prediction for a new case')
#

dia_m = 0.762		         # Input monopile diameter in m
Thickness_m = 0.014       # Input monopile thickness in m
Embedded_Length_m = 4.0  # Input monopile embedded_length in m
#
xinp = []
xtemp = []

for i in range(0,20):
    if i < 5:
        disp =  (dia_m*1000*0.15/100)*i/4    
        xtemp = [dia_m, Thickness_m, Embedded_Length_m, disp]
        xinp.append(xtemp)
    else:
        disp =  (dia_m*1000*0.15 - dia_m*1000*0.15/100)*(i-4)/15 + dia_m*1000*0.15/100  
        xtemp = [dia_m, Thickness_m, Embedded_Length_m, disp]
        xinp.append(xtemp)
        
xinp_df = pd.DataFrame(xinp, columns=["Dia_m", "Thickness_m", "Embedded length_m", "Ux_mm"])
print(xinp_df)

#
xinp_scaled = scaler.transform(xinp)
#
prediction_vec = svr_surrogate.predict(xinp_scaled)
#
results = xinp_df.copy()
#
results['Fx_kN'] = prediction_vec
results.to_csv(path_out)

#
plt.plot(results['Ux_mm'],results['Fx_kN'], color = 'black')
plt.title(f"Monopile Load-Displacement Curve")
plt.xlabel('Displacement (mm)')
plt.ylabel('Load (kN)')
plt.show()
