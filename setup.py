from setuptools import setup, find_packages

setup(
    name='Visual Novel Recommendation Engine',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scipy',
        'sklearn',
        'numpy'
    ],
    package_data={
        'vnrec': ['vn_titles', 'votes', 'tags_vn']
    }
)