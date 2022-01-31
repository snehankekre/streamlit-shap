import streamlit as st
import streamlit.components.v1 as components
import shap

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import base64
from io import BytesIO

def st_shap(plot, height=None):

    if plot is None:
        fig = plt.gcf()
        ax = plt.gca()

        buf = BytesIO()
        fig.savefig(buf, format="png")
        fig_width, fig_height = fig.get_size_inches()*fig.dpi

        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        html_str = f"<img src='data:image/png;base64,{data}'/>"
        plt.cla()
        plt.close(fig)

        fig = components.html(html_str, height=fig_height, width=fig_width)

    elif isinstance(plot, Figure):
        fig = plot
    
    else:
        shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
        fig = components.html(shap_html, height=height)
    
    return fig
