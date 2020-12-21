from setuptools import setup

setup(
    name='lias',
    version='0.1',
    packages=['lias'],
    url='https://github.com/OneOvano/LIAS',
    license='MIT',
    install_requires=(
        'numpy>=1.18.0',
        'pandas>=1.1.0',
        'scipy>=1.5.0',
        'lxml>=4.5.0',
        'matplotlib>=3.0.0',
        'PyQt5'
    ),
    test_suite='test',
    author='Vano',
    author_email='iv.shaposhnikov@gmail.com',
    description='Lines Identification in Astrophysical Spectra'
)
