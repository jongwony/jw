from setuptools import setup, find_packages


class Packages:
    crawl = ['requests', 'bs4']
    iterm = ['pygments', 'pyfiglet']
    all = crawl + iterm


setup(
    name='jw',
    version='0.4',
    description='I just want to search and write my notes'
                'regardless of their file name ...',
    author='jongwony',
    author_email='lastone9182@gmail.com',
    packages=find_packages(exclude=['tests*']),
    scripts=['jw'],
    install_requires=['sqlalchemy', 'pandas'],
    extras_require={k: v for k, v in Packages.__dict__.items()
                    if not k.startswith('__')},
    package_data={'bio': ['config.ini', 'templates/*', 'scripts/*']},
    url='https://github.com/jongwony/jw',
)
