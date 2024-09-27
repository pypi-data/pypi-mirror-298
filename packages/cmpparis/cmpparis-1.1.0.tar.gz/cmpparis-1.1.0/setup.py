####################################################
# setup.py for the 'cmpparis' library
# Created by: Sofiane Charrad
####################################################


import setuptools

with open("README_PYPI.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmpparis",
    version="1.1.0",
    author="Sofiane Charrad | Hakim Lahiani",
    author_email="s.charrad@cmp-paris.com |  h.lahiani@cmp-paris.com",
    description="Une bibliothèque pour CMP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codecatalyst.aws/spaces/CMP/projects/Coding-Tools/source-repositories/python-cmpparis-lib/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "moto",
        "paramiko"
    ]
)