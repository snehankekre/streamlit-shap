import streamlit as st
import shap
from streamlit_shap import st_shap
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

# Based on https://github.com/slundberg/shap/blob/master/notebooks/image_examples/image_classification/Image%20Multi%20Class.ipynb

st.set_page_config(layout="wide")

# load pre-trained model and data
model = ResNet50(weights='imagenet')
X, y = shap.datasets.imagenet50()

# getting ImageNet 1000 class names
url = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"
with open(shap.datasets.cache(url)) as file:
    class_names = [v[1] for v in json.load(file).values()]

# python function to get model output; replace this function with your own model function. 
def f(x):
    tmp = x.copy()
    preprocess_input(tmp)
    return model(tmp)

# define a masker that is used to mask out partitions of the input image. 
masker = shap.maskers.Image("inpaint_telea", X[0].shape)

# create an explainer with model and image masker 
explainer = shap.Explainer(f, masker, output_names=class_names)

# here we explain two images using 500 evaluations of the underlying model to estimate the SHAP values
shap_values = explainer(X[1:3], max_evals=100, batch_size=50, outputs=shap.Explanation.argsort.flip[:4]) 

col1, col2 = st.columns(2)

with col1:
    # output with shap values
    st_shap(shap.image_plot(shap_values), height=800, width=550)

with col2:
    st.code(
        """
import streamlit as st
import shap
from streamlit_shap import st_shap
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

# Based on https://github.com/slundberg/shap/blob/master/notebooks/image_examples/image_classification/Image%20Multi%20Class.ipynb

# load pre-trained model and data
model = ResNet50(weights='imagenet')
X, y = shap.datasets.imagenet50()

# getting ImageNet 1000 class names
url = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"
with open(shap.datasets.cache(url)) as file:
    class_names = [v[1] for v in json.load(file).values()]

# python function to get model output; replace this function with your own model function. 
def f(x):
    tmp = x.copy()
    preprocess_input(tmp)
    return model(tmp)

# define a masker that is used to mask out partitions of the input image. 
masker = shap.maskers.Image("inpaint_telea", X[0].shape)

# create an explainer with model and image masker 
explainer = shap.Explainer(f, masker, output_names=class_names)

# here we explain two images using 500 evaluations of the underlying model to estimate the SHAP values
shap_values = explainer(X[1:3], max_evals=100, batch_size=50, outputs=shap.Explanation.argsort.flip[:4]) 

# output with shap values
st_shap(shap.image_plot(shap_values), height=800, width=550)
""", language="python"
    )