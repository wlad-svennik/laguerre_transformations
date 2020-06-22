from distutils.core import setup
setup(
  name = 'laguerre_transformations',
  packages = ['laguerre_transformations'],
  version = '0.1',
  license='BSD-3-Clause',
  description = 'Visualize Laguerre transformations.',
  author = 'Ran Gutin',
  author_email = 'jkabrg@gmail.com',
  url = 'https://github.com/ogogmad/laguerre_transformations',
  download_url = 'https://github.com/ogogmad/laguerre_transformations/archive/v_01.tar.gz',
  keywords = ['mathematics', 'transformations', 'geometry', 'hypercomplex'],
  install_requires=[
          'scipy',
          'Pillow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Mathematicians',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: BSD-3-Clause',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)