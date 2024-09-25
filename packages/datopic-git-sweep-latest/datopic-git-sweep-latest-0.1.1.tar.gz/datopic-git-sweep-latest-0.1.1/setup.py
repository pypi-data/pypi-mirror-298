# import sys
# import os
# from setuptools import setup, find_packages
#
# here = os.path.abspath(os.path.dirname(__file__))
# README = open(os.path.join(here, 'README.rst')).read()
# NEWS = open(os.path.join(here, 'NEWS.txt')).read()
#
# version = '0.1.1'
#
# install_requires = [
#     'GitPython>=0.3.2RC1']
#
# # Add argparse if less than Python 2.7
# if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
#     install_requires.append('argparse>=1.2.1')
#
# setup(name='datopic-git-sweep-latest',
#     version=version,
#     description="Clean up branches from your Git remotes",
#     long_description=README + '\n\n' + NEWS,
#     classifiers=[
#         'Development Status :: 4 - Beta',
#         'Environment :: Console',
#         'License :: OSI Approved :: MIT License',
#         'Intended Audience :: Developers',
#         'Natural Language :: English',
#         'Operating System :: POSIX',
#         'Programming Language :: Python :: 2.6',
#         'Programming Language :: Python :: 2.7',
#         'Topic :: Software Development :: Quality Assurance',
#         'Topic :: Software Development :: Version Control',
#         'Topic :: Text Processing'
#     ],
#     keywords='git maintenance branches',
#     author='Arc90, Inc.',
#     author_email='',
#     url='http://arc90.com',
#     license='MIT',
#     packages=find_packages('src'),
#     package_dir = {'': 'src'},
#     include_package_data=True,
#     zip_safe=False,
#     install_requires=install_requires,
#     entry_points={
#         'console_scripts':
#             ['git-sweep=gitsweep.entrypoints:main']
#     }
# )

import sys
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Ensure README and NEWS files are optional
README = ''
NEWS = ''

if os.path.exists(os.path.join(here, 'README.md')):  # Assuming you're using Markdown
    with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
        README = f.read()

if os.path.exists(os.path.join(here, 'NEWS.txt')):
    with open(os.path.join(here, 'NEWS.txt'), 'r', encoding='utf-8') as f:
        NEWS = f.read()

version = '0.1.1'

install_requires = [
    'GitPython>=0.3.2RC1'
]

# Add argparse if Python version is less than 2.7
if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
    install_requires.append('argparse>=1.2.1')

setup(
    name='datopic-git-sweep-latest',
    version=version,
    description="Clean up branches from your Git remotes",
    long_description=README + '\n\n' + NEWS,
    long_description_content_type='text/markdown',  # Specify the content type explicitly
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Version Control',
        'Topic :: Text Processing'
    ],
    keywords='git maintenance branches',
    author='Arc90, Inc.',
    author_email='',
    url='http://arc90.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'git-sweep=gitsweep.entrypoints:main'
        ]
    }
)
