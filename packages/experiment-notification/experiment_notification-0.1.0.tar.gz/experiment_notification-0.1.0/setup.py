from setuptools import setup, find_packages

setup(
    name='experiment_notification',
    version='0.1.0',
    author='Steven Li',
    author_email='stevenazy@outlook.com',
    description='This package can send you an notification when your experiments are done!',
    packages=find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)