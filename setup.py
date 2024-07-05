from setuptools import setup, find_packages

HYPE_DOT = '-e .'
def get_requirements(file_str):

    with open(file_str) as obj:
        requirements = obj.readlines()
        requirements = [req.replace('\n','')for req in requirements]

        if HYPE_DOT in requirements:
            requirements.remove(HYPE_DOT)


setup(
    name='Hand Recongnition',
    author='Michael Romeo',
    author_email='romeo-michael@outlook.com',
    packages=find_packages(),
    requires=get_requirements(file_str = 'requirements.txt')
)