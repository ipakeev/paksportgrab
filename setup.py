from setuptools import setup, find_packages

setup(
    name='paksportgrab',
    version='0.3.13',
    packages=find_packages(),
    url='https://github.com/ipakeev',
    license='MIT',
    author='Ipakeev',
    author_email='ipakeev93@gmail.com',
    description='Lib for grab sport data', install_requires=['pakselenium', 'paklib', 'selenium', 'pytest']
)
