from setuptools import setup, find_packages


setup(
    name='seq_mutator',
    version='0.2.13',
    description='A toolbox for protein engineering and DNA shuffling',
    author='iGEM Team Muenster 2024',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author_email='j_albr16@uni-muenster.de',
    url='https://gitlab.igem.org/2024/software-tools/unimuenster',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    include_package_data=True,
    python_requires='>=3.10.11,<=3.10.12',
    entry_points={
        'console_scripts': [
            'seq_mutator = src.app:main'
        ]
    },
)

