from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="sdcf",
    version="0.2.0",
    author="Shankar Dutt",
    author_email="shankar.dutt@anu.edu.au",
    description="Shankar Dutt's Carbon Fibre Strength Testing Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "sdcf=sdcf.cli:main",
        ],
    },
    install_requires=[
        "streamlit",
        "numpy",
        "pandas",
        "matplotlib",
        "plotly",
        "scipy",
        "pdfkit"
    ],
    python_requires=">=3.10",
)