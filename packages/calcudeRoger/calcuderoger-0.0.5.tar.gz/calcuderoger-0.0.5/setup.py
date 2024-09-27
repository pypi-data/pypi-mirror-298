from setuptools import setup, find_packages


setup( 
    name='calcudeRoger', 
    version='0.0.5',
    packages=['calcudeRoger.otrom'],
    author='Roger', 
    description= 'Simple test package', 
    long_description=open("README.rst","r", encoding="utf-8").read(),
    install_requires=['CoolProp'],
)
