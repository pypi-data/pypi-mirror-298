from setuptools import setup, find_packages

setup(
    name="healthviz",  
    version="0.1.1",  
    description="A package for health data visualization and analysis",
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url="https://github.com/Saunakghosh10",  
    author="Saunak Ghosh",  # Your
    author_email="saunakofficial10@gmail.com",  
    license="MIT",  
    packages=find_packages(), 
    install_requires=[  
        "pandas",
        "matplotlib",
        "seaborn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
