import streamlit as st
import shap
from streamlit_shap import st_shap
import transformers

# Based on https://github.com/slundberg/shap/blob/master/notebooks/text_examples/sentiment_analysis/Positive%20vs.%20Negative%20Sentiment%20Classification.ipynb
@st.experimental_singleton
def load_model(model_name="distilbert-base-uncased-finetuned-sst-2-english"):
    model = transformers.pipeline('sentiment-analysis', model=model_name, return_all_scores=True)
    return model

@st.experimental_memo
def load_explainer(_model):
    explainer = shap.Explainer(model)
    return explainer

@st.experimental_memo
def load_shap_values(_explainer, sentence):
    shap_values = explainer([sentence])
    return shap_values


model = load_model()
explainer = load_explainer(model)

sentence = st.text_input("Enter a sentence to explain:")

if sentence:
    shap_values = load_shap_values(explainer, sentence)
    st.markdown("### Explanation for the POSITIVE output class")
    st_shap(shap.plots.text(shap_values[0, :, "POSITIVE"]))

    st.markdown("### Explanation for the NEGATIVE output class")
    st_shap(shap.plots.text(shap_values[0, :, "NEGATIVE"]))