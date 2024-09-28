from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hitl_al_gomg",
    version="0.0.9",
    license="MIT",
    author="Yasmine Nahal",
    author_email="yasmine.nahal@aalto.fi",
    description="A Human-in-the-loop active learning workflow to improve molecular property predictors with human expert feedback for goal-oriented molecule generation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yasminenahal/hitl_al_gomg.git",
    keywords = ['REINVENT', 'HITL', 'HITL_AL_GOMG'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9,<3.11",
    install_requires=[  # Add your dependencies here
        "torch==1.12.1",
        "click==8.1.7",
        "scipy==1.10.1",
        "rdkit-pypi==2022.9.5",
        "pyTDC==1.0.7",
        "fcd_torch==1.0.7",
        "matplotlib==3.9.2",
        "jupyter==1.1.1",
    ],
)