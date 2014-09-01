# -*- coding: utf-8 -*-

import os
import setuptools

setuptools.setup(
  name='owf2014',
  version='0.1dev',
  url='http://www.openworldforum.org/',
  license='LGPL',
  author='Stefane Fermigier',
  author_email='sf@fermigier.com',
  description='The site for the Open World Forum 2014',
  long_description=__doc__,
  packages=['website'],
  zip_safe=False,
  platforms='any',
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    ],
)
