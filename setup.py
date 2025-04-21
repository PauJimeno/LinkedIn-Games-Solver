from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='linkedin-games-solver',
    version='1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'zip_solver=base.ZipSetup:main',
            'queens_solver=base.QueensSetup:main'
        ],
    },
)
