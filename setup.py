from setuptools import setup

setup(name='MopsOverexert', version='1.0',
      description='OpenShift Python-3.3 Community Cartridge based application',
      author='Lars Kellogg-Stedman', author_email='lars@oddbit.com',

      #  Uncomment one or more lines below in the install_requires section
      #  for the specific client drivers/modules your application needs.
      install_requires=[
          'bottle',
          'requests',
          'pystache',
          'markdown',
          'PyYAML',
          'beaker',
      ],
     )
