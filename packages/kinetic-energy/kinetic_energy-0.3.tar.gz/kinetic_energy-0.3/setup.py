from setuptools import setup , find_packages 
with open("README.md" ,"r") as f:
    description=f.read()
setup (
    name='kinetic_energy',
    version='0.3',
    packages=find_packages(),
    install_requires= [
        'numpy>1.11.1'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
    

)