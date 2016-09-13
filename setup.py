import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid == 1.7',
    'pyramid_chameleon == 0.3',
    'pyramid_jinja2 == 2.6.2',
    'pyramid_debugtoolbar == 3.0.2',
    'waitress == 1.0a1',
    'pyramid_sacrud == 0.3.3',
    'sqlalchemy == 1.1.0b2',
    'pyramid_tm == 0.12.1',
    'psycopg2 == 2.6.2',
    'alembic == 0.8.6',
    'zope.sqlalchemy == 0.7.7',
    'pyramid_ipython == 0.2',
    'pyyaml == 3.12',
    ]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

setup(name='bible_drevle_com',
      version='0.1',
      description='bible_drevle_com',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = bible_drevle_com:main
      """,
      )
