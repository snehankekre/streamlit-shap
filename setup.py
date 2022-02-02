import setuptools

setuptools.setup(
    name="streamlit-shap",
    version="0.0.4",
    author="Snehan Kekre",
    author_email="snehan@streamlit.io",
    description="Streamlit component for SHAP",
    long_description="Streamlit component for SHAP (SHapley Additive exPlanations)",
    long_description_content_type="text/plain",
    url="https://github.com/snehankekre/streamlit-shap",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=["streamlit >= 1.0.0", "shap >= 0.4.0", "matplotlib >= 3.0.2, <= 3.4.3"],
)
