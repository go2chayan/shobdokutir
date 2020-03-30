"""
Simple check list from AllenNLP repo: https://github.com/allenai/allennlp/blob/master/setup.py

To create the package for pypi.

1. Change the version in __init__.py and setup.py.

2. Commit these changes with the message: "Release: VERSION"

3. Add a tag in git to mark the release: "git tag VERSION -m'Adds tag VERSION for pypi' "
   Push the tag to git: git push --tags origin master

4. Build both the sources and the wheel. Do not change anything in setup.py between
   creating the wheel and the source distribution (obviously).

   For the wheel, run: "python setup.py bdist_wheel" in the top level allennlp directory.
   (this will build a wheel for the python version you use to build it - make sure you use python 3.x).

   For the sources, run: "python setup.py sdist"
   You should now have a /dist directory with both .whl and .tar.gz source versions of allennlp.

5. Check that everything looks correct by uploading the package to the pypi test server:

   twine upload dist/* -r pypitest
   (pypi suggest using twine as other methods upload files via plaintext.)

   Check that you can install it in a virtualenv by running:
   pip install -i https://testpypi.python.org/pypi allennlp

6. Upload the final version to actual pypi:
   twine upload dist/* -r pypi

7. Copy the release notes from RELEASE.md to the tag in github once everything is looking hunky-dory.

"""

from setuptools import setup, find_packages
import re
from io import open

def get_version():
    """
    Extract the version from the module's root __init__.py file
    """
    root_init_file = open("shobdokutir/__init__.py").read()
    match = re.search("__version__[ ]+=[ ]+[\"'](.+)[\"']", root_init_file)
    return match.group(1) if match is not None else "unknown"

setup(
    name="shobdokutir",
    version=get_version(),
    author="Md Iftekhar Tanveer",
    author_email="go2chayan@gmail.com",
    description="A comprehensive Natural Language Processing (NLP) suite for Bangla and other low-resource Language",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",

    packages=find_packages(),

    package_data={},

    python_requires='>=3.7',

    install_requires=['flask',
                      'selenium==4.0.0a3',
                      'bs4',
                      'lxml',
                      'pyaml',
                      'requests',
                      'numpy',
                      'nltk',
                      'pillow',
                      'pdfminer'],

    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)

