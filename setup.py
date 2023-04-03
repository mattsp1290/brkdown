from setuptools import setup, find_packages

setup(
    name='brkdown',
    version=0.2,
    package_dir={'brkdown': 'src'},
    packages=find_packages(),
    install_requires=[
        'Click',
        'librosa',
        'numpy'
        'pydub',
        'soundfile'
    ],
    entry_points='''
        [console_scripts]
        brkdown=src.main:cli
    '''
)