from setuptools import setup, find_packages

setup(
    name='rknn',
    version='0.1',
    packages=find_packages(),
    install_requires=['numpy'],
    description='A k-NN classifier using generalized social distance metrics',
    author='Ram Jeevan ',
    author_email='b.k.r.jeevan@gmail.com',
)
