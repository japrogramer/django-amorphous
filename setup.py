import os
from setuptools import setup, find_packages

CURRENT_DIR = os.path.dirname(__file__)
def read(fname):
    return open(os.path.join(CURRENT_DIR, fname)).read()

# Info for setup
PACKAGE = 'amorphous'
NAME = 'django-amorphous'
DESCRIPTION = 'django-amorphous unlocks the power of JsonField'
AUTHOR = 'Jorge Perez'
AUTHOR_EMAIL = 'japrogramer@gmail.com'
URL = 'https://github.com/japrogramer/django-amorphous'
VERSION = __import__(PACKAGE).__version__

# setup call
setup(
    name=NAME,
    packages = find_packages(),
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README.rst'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='BSD',
    url=URL,
    # packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
         'Development Status :: 3 - Alpha',
         'Environment :: Web Environment',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: BSD License',
         'Operating System :: OS Independent',
         'Programming Language :: Python',
         'Framework :: Django',
    ],
    keywords = 'django json JsonField amorphous',
    install_requires = [
         'django>=1.8',
         'pytz>=2014.2',
    ],
    zip_safe=False,
    )
