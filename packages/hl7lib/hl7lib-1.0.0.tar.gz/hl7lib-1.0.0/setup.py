from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='hl7lib',
      version='1.0.0',
      description='HL7 message parser',
      long_description=readme(),
      keywords='hl7 parsing ',
      url='https://github.com/norlowski/HL7py',
      author='fatryst',
      author_email='fatryst@gmail.com',
      license='MIT',
      packages=['hl7lib'],
      zip_safe=False)
