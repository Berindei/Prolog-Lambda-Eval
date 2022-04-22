from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='LambdaEval',
    version='0.1.0',
    description='LambdaEval',
    long_description="readme",
    author='Matei Chesa',
    author_email='mic35@cam.ac.uk',
    #url='https://gitlab.developers.cam.ac.uk/mic35/smart-project/',
    license="license",
    packages=find_packages(exclude=('tests', 'docs'))
)
