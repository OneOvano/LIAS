from setuptools import setup, find_packages

setup(name='lias',
      version='0.1',
      description='Lines Indentification in Astrophysical Spectra',
      long_description='Tool for line identification in spectra of astrophysical objects',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7.3',
      ],
      keywords='astrophysics, spectra',
      url='https://github.com/OneOvano/LIAS',
      author='Vano',
      author_email='iv.shaposhnikov@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requirements',
      ])
