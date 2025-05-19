from joblib import load
import os

# relative path to input folder data
model_folder = r"model"
# paths to 
path_model  = os.path.abspath(os.path.join(model_folder, "svr_monopile_wholecurve.joblib"))
path_scaler = os.path.abspath(os.path.join(model_folder, "svr_scaling_monopile_wholecurve.joblib"))

svr_surrogate = load(path_model)
scaler = load(path_scaler)

def predict_Fx(dia_m, thk_m, embed_length_m):
    """
    Function to predict the load-displacement curve of a monopile using loaded surrogate model.
    Parameters
    ----------
    dia_m : float
        Diameter of the monopile in meters.
    thk_m : float
        Thickness of the monopile in meters.
    embed_length_m : float
        Embedded length of the monopile in meters.
    Returns
    -------
    predicted_Fx_kN : list
        List of predicted load values in kN.
    """

    xinp = []
    
    for i in range(0,20):
        if i < 5:
            disp =  (dia_m*1000*0.15/100)*i/4    
            xtemp = [dia_m, thk_m, embed_length_m, disp]
            xinp.append(xtemp)
        else:
            disp =  (dia_m*1000*0.15 - dia_m*1000*0.15/100)*(i-4)/15 + dia_m*1000*0.15/100  
            xtemp = [dia_m, thk_m, embed_length_m, disp]
            xinp.append(xtemp)
    
    # scale the input data
    xinp_scaled = scaler.transform(xinp)
    
    # predict the output using the surrogate model
    predicted_Fx_kN = svr_surrogate.predict(xinp_scaled)
    input_disp = [i[3] for i in xinp]

    return input_disp, predicted_Fx_kN