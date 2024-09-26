from setuptools import setup, find_packages

setup(
    name="datafuncs",
    version="0.3.5",
    author="Fraser Woodward and Liam Leonard",
    author_email="woodwardfraser1@gmail.com, liamleonard@outlook.ie",
    description="Functions for Data Processing",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Liam-Leonard/Data-Funcs",
    project_urls={
        "Bug Tracker": "https://github.com/Liam-Leonard/Data-Funcs/issues",
        "Documentation": "https://github.com/Liam-Leonard/Data-Funcs",
    },
)
