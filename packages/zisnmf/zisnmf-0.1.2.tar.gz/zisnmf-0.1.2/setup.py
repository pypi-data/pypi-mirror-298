from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='zisnmf',
    version='0.1.2',
    description='Zero-inflated Supervised Non-negative Matrix Factorization',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Feng Zeng',
    author_email='zengfeng@xmu.edu.cn',
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.9.2',
        'numpy>=2.0.2',
        'pandas>=2.2.2',
        'pyro_ppl>=1.9.1',
        'scanpy>=1.10.3',
        'scikit_learn>=1.5.2',
        'scipy>=1.13.1',
        'seaborn>=0.13.2',
        'setuptools>=73.0.1',
        'torch>=2.3.1',
        'tqdm>=4.66.5'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)