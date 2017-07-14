
import re
import sys
import setuptools


def get_version(path="src/dyspatch/__init__.py"):
    """ Return the version of by with regex intead of importing it"""
    init_content = open(path, "rt").read()
    pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
    return re.search(pattern, init_content, re.M).group(1)


def get_requirements(path):

    setuppy_format = \
        'https://github.com/{user}/{repo}/tarball/master#egg={egg}'

    setuppy_pattern = \
        r'github.com/(?P<user>[^/.]+)/(?P<repo>[^.]+).git#egg=(?P<egg>.+)'

    dep_links = []
    install_requires = []
    with open(path) as f:
        for line in f:

            if "sys_platform" in line:
                line, platform = line.split(';')

                match = re.search(r'sys_platform\s*==\s*(.*)', platform)

                if sys.platform != match.groups()[0].strip('\"\''):
                    continue

            if line.startswith('-e'):
                url_infos = re.search(setuppy_pattern, line).groupdict()
                dep_links.append(setuppy_format.format(**url_infos))
                line = '=='.join(url_infos['egg'].rsplit('-', 1))

            install_requires.append(line.strip())

    return install_requires, dep_links


requirements, _ = get_requirements('requirements.txt')
dev_requirements, _ = get_requirements('dev-requirements.txt')


setuptools.setup(name='dyspatch',
                 version=get_version(),
                 description=('Framework providing dispatchers primitives and '
                              'systems, e.g: event handlers, routing, etc.'),
                 long_description=open('README.rst').read().strip(),
                 author='Sam & Max',
                 author_email='lesametlemax@gmail.com',
                 url='https://github.com/sametmax/dyspatch/',
                 packages=setuptools.find_packages('src'),
                 package_dir={'': 'src'},
                 install_requires=requirements,
                 extras_require={
                     'dev': dev_requirements
                 },
                 setup_requires=['pytest-runner'],
                 tests_require=dev_requirements,
                 include_package_data=True,
                 license='WTFPL',
                 zip_safe=False,
                 keywords='dyspatch events signals routing',
                 classifiers=['Development Status :: 1 - Planning',
                              'Intended Audience :: Developers',
                              'Natural Language :: English',
                              'Programming Language :: Python :: 3.4',
                              'Programming Language :: Python :: 3 :: Only',
                              'Operating System :: OS Independent'],)
