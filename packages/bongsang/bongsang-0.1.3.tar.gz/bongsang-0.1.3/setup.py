# setup.py

from setuptools import setup, find_packages

setup(
    name='bongsang',  # Package name is 'bongsang'
    version='0.1.3',
    author='Bongsang Kim',
    author_email='happykbs@gmail.com',
    description='A collection of statistics and machine learning libraries under the bongsang package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bongsang/bongsang',  # Update with your repository URL
    packages=find_packages(),
    include_package_data=True,  # Include package data specified in MANIFEST.in
    package_data={
        'bongsang.datasets': ['*.csv'],
    },
    install_requires=[
        'numpy>=1.18.0',
        'pandas>=1.0.0',
        'matplotlib>=3.0.0',
        'scikit-learn>=0.22.0',
        'scipy>=1.4.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
