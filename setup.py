from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup


def read(f):
    try:
        with open(f, "r") as h:
            return h.read()
    except IOError:
        return ""


install_reqs = [
    l for l in read("requirements.txt").splitlines() if not l.startswith("#")
]

setup(
    name="django-gss-spnego",
    version="19.02.0dev",
    url="https://github.com/imc-trading/django-gss-spnego.git",
    description="Django GSSAPI SPNEGO",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    author="Brandon Ewing",
    author_email="brandon.ewing@imc.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    install_requires=install_reqs,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
