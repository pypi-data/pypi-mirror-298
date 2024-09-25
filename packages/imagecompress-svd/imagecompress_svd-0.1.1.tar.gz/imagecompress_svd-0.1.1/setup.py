from setuptools import setup, find_packages

setup(
    name='imagecompress_svd',
    version='0.1.1',
    packages=find_packages(),
    description='A Python package for image compression using Singular Value Decomposition (SVD).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'pillow',
        'scipy',
        'scikit-learn',
    ],
    author='Katie Wen-Ling Kuo',
    author_email='katie20030705@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)