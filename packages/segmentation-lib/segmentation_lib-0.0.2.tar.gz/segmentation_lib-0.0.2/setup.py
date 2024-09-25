from setuptools import setup, find_packages


with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name='segmentation_lib',
    version='0.0.2',
    description='Library for images segmentation',
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PavelMalyshev01/segmentation_lib',
    author='Pavel Malyshev',
    author_email='p.malyshev@razumai.pro',
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'torch',
        'torchvision',
        'pillow',
        'numpy',
        'pandas',
        'opencv-python',
        'albumentations',
        'tqdm',
        'matplotlib',
        'plotly',
        'PrettyTable',
        'dill',
        'optuna',
        'pathlib',
        'os'
    ],
    extras_requre={
        "dev": ["pytest>=7.0", "twine>=4.0.2"]
    },
    python_requires='>=3.6',
)
