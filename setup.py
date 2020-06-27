from distutils.core import setup
setup(
  name = 'laguerre_transformations',
  packages = ['laguerre_transformations'],
  version = '0.3',
  license='BSD-3-Clause',
  description = 'Visualize Laguerre transformations.',
  author = 'Ran Gutin',
  author_email = 'jkabrg@gmail.com',
  url = 'https://github.com/ogogmad/laguerre_transformations',
  download_url = 'https://github.com/ogogmad/laguerre_transformations/archive/v_03.tar.gz',
  keywords = ['mathematics', 'transformations', 'geometry', 'hypercomplex'],
  install_requires=[
          'scipy',
          'Pillow',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
