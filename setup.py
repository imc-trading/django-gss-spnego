from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup

def read(f):
    try:
        with open(f, "r") as h:
            return h.read()
    except IOError:
        return ''


install_reqs = [l for l in read("requirements.txt").splitlines() if not l.startswith("#")]

setup(
    name='django-gss-spnego',
    version="0.0.1",
    url='',
    license='',
    description='',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Brandon Ewing',
    author_email='brandon.ewing@warningg.com',
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    install_requires=install_reqs,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
