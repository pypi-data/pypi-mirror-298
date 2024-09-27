#!/usr/bin/env python3

import io
import os
from os import path, walk

from setuptools import setup, find_packages

with io.open('README.pypi', 'r', encoding='utf-8') as f:
    ABOUT = f.read()

NAME = 'Blauwal3-ImageAnalytics'

MAJOR = 0
MINOR = 12
MICRO = 4
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

AUTHOR = '大圣实验楼'
AUTHOR_EMAIL = 'dashenglab@163.com'

URL = 'http://orange.biolab.si/download'
DESCRIPTION = '用于图像数据挖掘的蓝鲸插件。'
LONG_DESCRIPTION = ABOUT
LICENSE = 'GPL3+'

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3 :: Only'
]

KEYWORDS = [
    'orange3 add-on',
    'orange3-imageanalytics'
]

PACKAGES = find_packages()

PACKAGE_DATA = {
    'orangecontrib.imageanalytics.widgets': ['icons/*.svg'],
    'orangecontrib.imageanalytics.widgets.tests': ['test_images/*'],
    'orangecontrib.imageanalytics.tests': ['test_images/*', 'test_images/img/*', 'test_images/img/inner/*'],
    'orangecontrib.imageanalytics': ['locale/*.yml'],
}

ENTRY_POINTS = {
    'orange.widgets':
        ('Image Analytics = orangecontrib.imageanalytics.widgets',),
    'orange3.addon':
        ('Orange3-Imageanalytics = orangecontrib.imageanalytics',),
    # Register widget help
    "orange.canvas.help": (
        'html-index = orangecontrib.imageanalytics.widgets:WIDGET_HELP_PATH',)
}

DATA_FILES = [
    # Data files that will be installed outside site-packages folder
]


def include_documentation(local_dir, install_dir):
    global DATA_FILES
    # if 'bdist_wheel' in sys.argv and not path.exists(local_dir):
    #     print("Directory '{}' does not exist. "
    #           "Please build documentation before running bdist_wheel."
    #           .format(path.abspath(local_dir)))
    #     sys.exit(0)
    doc_files = []
    for dirpath, dirs, files in walk(local_dir):
        doc_files.append((dirpath.replace(local_dir, install_dir),
                          [path.join(dirpath, f) for f in files]))
    DATA_FILES.extend(doc_files)


if __name__ == '__main__':
    include_documentation('doc/_build/html', 'help/orange3-imageanalytics')
    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        license=LICENSE,
        packages=PACKAGES,
        data_files=DATA_FILES,
        package_data=PACKAGE_DATA,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        install_requires=[
            "AnyQt",
            "ndf >=0.1.4",
            "numpy >=1.16",
            'Blauwal3>=3.38.0',
            'Blauwal3-widget-base',
            "Blauwal3-canvas-core",
            "pillow >=6.2.0",
            "requests",
            "requests_cache",
            "scipy",
        ],
        extras_require={
            'test': ['coverage', ],
            'doc': ['sphinx', 'recommonmark', 'sphinx_rtd_theme', ],
        },
        namespace_packages=['orangecontrib'],
        entry_points=ENTRY_POINTS,
    )
