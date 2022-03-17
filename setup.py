import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamlit-shap",
    version="1.0.1",
    author="Snehan Kekre",
    author_email="snehan@streamlit.io",
    description="Streamlit component for SHAP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snehankekre/streamlit-shap",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["shap >= 0.4.0"],
)
