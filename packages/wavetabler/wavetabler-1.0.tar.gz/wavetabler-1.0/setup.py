from setuptools import setup, find_packages

setup(
    name='wavetabler',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'librosa',
        'resampy',
        'soundfile',
        'pydub',
        'matplotlib',
        'pandas',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'wvtbl=wvtbl:main',
        ],
    },
    description='Wavetabler: A tool for generating wavetables from audio files',
    author='Your Name',
    license='MIT',
)
