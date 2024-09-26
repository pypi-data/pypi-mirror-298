from setuptools import setup, find_packages

VERSION = "0.2.2"

setup(
    name="dropdown_filters",  
    version=VERSION,  
    description="Reusable Django admin filters",  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    author="Diego Piedra",
    author_email="diego@dieveloper.com",
    url="https://github.com/DiegoP2001/Dropdown_filters",  
    packages=find_packages(),  
    include_package_data=True, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django>=2.0.8",  
    ],
)
