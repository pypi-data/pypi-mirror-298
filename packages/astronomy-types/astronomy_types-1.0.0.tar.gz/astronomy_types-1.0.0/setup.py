from setuptools import setup

setup(
    name="astronomy_types", 
    version="1.0.0",
    py_modules=["astronomy_typest"],  # without .py
    author="Artur Foden",
    author_email="",
    description="Type hints for Python astronomy projects",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Arturius771/astronomy_types", 
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.12.4',
)
