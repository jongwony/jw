from setuptools import setup, find_packages

setup(
    name='bio',
    version='1.0',
    description='I just want to search and write my notes'
                'regardless of their file name ...',
    author='jongwony',
    author_email='lastone9182@gmail.com',
    packages=find_packages(exclude=['tests*']),
    scripts=['biocli'],
    install_requires=['elasticsearch>=6.3.1', 'elasticsearch-dsl==6.3.1',
                      'requests', 'bs4', 'sqlalchemy', 'pandas'],
    package_data={'bio': ['config.ini', 'templates/*', 'scripts/*']},
    url='https://github.com/jongwony/bio',
)
