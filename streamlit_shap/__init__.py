import streamlit as st
import streamlit.components.v1 as components
import shap

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import base64
from io import BytesIO


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
            plt.tight_layout()

            # Save it to a temporary buffer
            buf = BytesIO()
            fig.savefig(buf, format="png")
            fig_width, fig_height = fig.get_size_inches() * fig.dpi

            # Embed the result in the HTML output
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            html_str = f"<img src='data:image/png;base64,{data}'/>"

            # Enable pyplot to properly clean up the memory
            plt.cla()
            plt.close(fig)

            fig = components.html(html_str, height=fig_height, width=fig_width)
        else:
            fig = components.html(
                "<p>[Error] No plot to display. Received object of type &lt;class 'NoneType'&gt;.</p>"
            )

    # SHAP plots return a matplotlib.figure.Figure object when passed show=False as an argument
    elif isinstance(plot, Figure):
        fig = plot
        plt.tight_layout()

        # Save it to a temporary buffer
        buf = BytesIO()
        fig.savefig(buf, format="png")
        fig_width, fig_height = fig.get_size_inches() * fig.dpi

        # Embed the result in the HTML output
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        html_str = f"<img src='data:image/png;base64,{data}'/>"

        # Enable pyplot to properly clean up the memory
        plt.cla()
        plt.close(fig)

        fig = components.html(html_str, height=fig_height, width=fig_width)

    # SHAP plots containing JS/HTML have one or more of the following callable attributes
    elif hasattr(plot, "html") or hasattr(plot, "data") or hasattr(plot, "matplotlib"):

        shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
        fig = components.html(shap_html, height=height, width=width)

    else:
        fig = components.html(
            "<p>[Error] No plot to display. Unable to understand input.</p>"
        )

    return fig
