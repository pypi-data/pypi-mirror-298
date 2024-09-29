from setuptools import setup, find_packages

setup(
    name="kryptograpi",                  
    version="0.4",                      
    packages=find_packages(),          
    install_requires=[],
    description="A library using mpmath and requests",
    long_description=open('README.md').read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/swupel/kryptograpi",  
    author="Anton Graller",                
    author_email="anton.graller@swupelpms.com", 
    license="MIT",                     
    classifiers=[                       
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
