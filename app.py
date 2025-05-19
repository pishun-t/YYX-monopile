import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from surrogate import predict_Fx

##### Initialise streamlit app #####
st.set_page_config(
    page_title="Surrogate test",
    page_icon=":bar_chart:", # bar chart emoji
)

st.title("Yunxiang's surrogate")
st.header("Monopile Load-Displacement Curve Prediction")

sel_D = st.slider(r"Diameter (m)", min_value=0.5, max_value=2.5, value=2.0, step=0.05)
sel_Dt = st.slider(r"D/t ratio", min_value=30., max_value=100., value=50., step=1.)
sel_LD = st.slider(r"L/D ratio", min_value=3., max_value=10., value=4., step=0.1)

t = sel_D / sel_Dt
L = sel_LD * sel_D

disp, Fx = predict_Fx(sel_D, t, L)

fig = px.line(
    x=disp,
    y=Fx,
    labels={'x': 'Displacement (mm)', 'y': 'Load (kN)'},
    title='Monopile Load-Displacement Curve'
)

st.plotly_chart(fig, use_container_width=True)