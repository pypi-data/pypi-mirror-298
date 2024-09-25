from setuptools import setup, find_packages

setup(
    name='Mensajes-jm.alvarez.dev',
    version='5.0',
    description='Un paquete para saludar y despedir',
    author='Jose Matias Alvarez',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author_email='jm.alvarez.dev@gmail.com',
    url='',
    lice_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite="tests",
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()],

    classifiers=['Environment :: Console']

)