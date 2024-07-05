from setuptools import find_packages, setup
from typing import List

HYPE_E_DOT = '-e .'
def get_requirements(file_path:str)->List:

    requirements = []
    with open(file_path) as obj:
        requirements = obj.readlines()
        requirements = [req.replace("\n","")for req in requirements]
        
        if HYPE_E_DOT  in requirements:
            requirements.remove(HYPE_E_DOT )

setup(
    name='Hand_recognition',
    version='0.1',
    author='Michael Romeo',
    author_email='romeo-michael@outlook.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)