from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='experiment_notification',
    version='0.1.1',
    author='Steven Li',
    author_email='stevenazy@outlook.com',
    description='This package can send you an notification when your experiments are done!',
     long_description=long_description, 
    long_description_content_type="text/markdown",  
    packages=find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)