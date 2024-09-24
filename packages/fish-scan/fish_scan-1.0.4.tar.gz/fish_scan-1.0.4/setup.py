#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

def main():

    setuptools.setup(
        name             = "fish-scan",
        version          = "1.0.4",
        description      = "",
        url              = "https://github.com/ariannaravera/fish-scan",
        author           = "Arianna Ravera",
        author_email     = "ariannaravera22@gmail.com",
        classifiers = [
            "Development Status :: 2 - Pre-Alpha",
            "Framework :: napari",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Scientific/Engineering :: Image Processing",
        ],
        dependencies = [
            "numpy",
            "magicgui",
            "qtpy",
            "scikit-image",
            "opencv-python",
            "matplotlib",
            "scikit-learn"
        ],
        include_package_data=True,
        package_data={
            'src/fish_scan/support_files': ['*.png'],
            "": ["src/fish_scan/support_files/*"],
        },
    )

if __name__ == "__main__":
    main()
