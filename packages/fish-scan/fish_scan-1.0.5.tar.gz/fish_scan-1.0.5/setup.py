#!/usr/bin/python
# -*- coding: utf-8 -*-

import setuptools

def main():

    setuptools.setup(
        name             = "fish-scan",
        version          = "1.0.5",
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
        packages=setuptools.find_packages(where="src"),
        package_dir={"": "src"},
        include_package_data=True
        )

if __name__ == "__main__":
    main()
