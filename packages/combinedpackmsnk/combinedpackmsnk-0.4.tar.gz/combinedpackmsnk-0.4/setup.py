from setuptools import setup, find_packages

setup(
    name='combinedpackmsnk',
    version='0.4',  # Increment the version number
    description='A comprehensive package for data analysis, visualization, preprocessing, and machine learning to minimize code and maximize insights.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='mukund14',
    author_email='mukundan.sankar14@gmail.com',
    url='https://pypi.org/project/combinedpackmsnk/',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'xgboost',
        'statsmodels',
        'plotly',
        'requests',
        'ydata-profiling'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)
