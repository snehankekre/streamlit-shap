import streamlit as st
import streamlit.components.v1 as components
import shap

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Prevent clipping of the ticks and axis labels
plt.rcParams['figure.autolayout'] = True

import base64
from io import BytesIO

# Shap plots internally call plt.show()
# On Linux, prevent plt.show() from emitting a non-GUI backend warning.
import os
os.environ.pop("DISPLAY", None)

# Note: Colorbar changes (introduced bugs) in matplotlib>3.4.3
# cause the colorbar of certain shap plots (e.g. beeswarm) to not display properly
# See: https://github.com/matplotlib/matplotlib/issues/22625 and
# https://github.com/matplotlib/matplotlib/issues/22087
# If colorbars are not displayed properly, try downgrading matplotlib to 3.4.3

def st_shap(plot, height=None, width=None):
    """Takes a SHAP plot as input, and returns a streamlit.delta_generator.DeltaGenerator as output.

    It is recommended to set the height and width
    parameter to have the plot fit to the window.

    Parameters
    ----------
    plot : None or matplotlib.figure.Figure or SHAP plot object
        The SHAP plot object.
    height: int or None
        The height of the plot in pixels.
    width: int or None
        The width of the plot in pixels.

    Returns
    -------
    streamlit.delta_generator.DeltaGenerator
        A SHAP plot as a streamlit.delta_generator.DeltaGenerator object.
    """

    # Plots such as waterfall and bar have no return value
    # They create a new figure and call plt.show()
    if plot is None:

        # Test whether there is currently a Figure on the pyplot figure stack
        # A Figure exists if the shap plot called plt.show()
        if plt.get_fignums():
            fig = plt.gcf()
            ax = plt.gca()

            # Save it to a temporary buffer
            buf = BytesIO()

            if height is None:
                _, height = fig.get_size_inches() * fig.dpi

            if width is None:
                width, _ = fig.get_size_inches() * fig.dpi

            fig.set_size_inches(width / fig.dpi, height / fig.dpi, forward=True)
            fig.savefig(buf, format="png")

            # Embed the result in the HTML output
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            html_str = f"<img src='data:image/png;base64,{data}'/>"

            # Enable pyplot to properly clean up the memory
            plt.cla()
            plt.close(fig)

            fig = components.html(html_str, height=height, width=width)
        else:
            fig = components.html(
                "<p>[Error] No plot to display. Received object of type &lt;class 'NoneType'&gt;.</p>"
            )

    # SHAP plots return a matplotlib.figure.Figure object when passed show=False as an argument
    elif isinstance(plot, Figure):
        fig = plot

        # Save it to a temporary buffer
        buf = BytesIO()

        if height is None:
            _, height = fig.get_size_inches() * fig.dpi

        if width is None:
            width, _ = fig.get_size_inches() * fig.dpi
        
        fig.set_size_inches(width / fig.dpi, height / fig.dpi, forward=True)
        fig.savefig(buf, format="png")

        # Embed the result in the HTML output
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        html_str = f"<img src='data:image/png;base64,{data}'/>"

        # Enable pyplot to properly clean up the memory
        plt.cla()
        plt.close(fig)

        fig = components.html(html_str, height=height, width=width)

    # SHAP plots containing JS/HTML have one or more of the following callable attributes
    elif hasattr(plot, "html") or hasattr(plot, "data") or hasattr(plot, "matplotlib"):

        shap_js = f"{shap.getjs()}".replace('height=350', f'height={height}').replace('width=100', f'width={width}')
        shap_html = f"<head>{shap_js}</head><body>{plot.html()}</body>"
        fig = components.html(shap_html, height=height, width=width)

    else:
        fig = components.html(
            "<p>[Error] No plot to display. Unable to understand input.</p>"
        )

    return fig
