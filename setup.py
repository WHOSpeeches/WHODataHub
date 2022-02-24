from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

with open('README.md', 'r') as fh:
    long_description = fh.read()

def custom_command(n):
    print(f'----------------- hello - {n} ----------------')


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        custom_command(1)

class CustomDevelopCommand(develop):
    def run(self):
        develop.run(self)
        custom_command(2)

class CustomEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)
        custom_command(3)

setup(
    name = "WHOSpeeches",
    version = "0.2.0",
    author = '@markanewman, @drstannwoji2019',
    author_email = 'whospeeches@trinetteandmark.com',
    description = 'Gen 2 service for retrieving the WHO''s Director General''s Speeches',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "https://github.com/WHOSpeechAnalysis/data",
    project_urls = {
        'Bug Reports': 'https://github.com/WHOSpeechAnalysis/data/issues',
        'Source': 'https://github.com/WHOSpeechAnalysis/data',
    },
    packages = ['WHOSpeeches'],
    package_dir = {'': 'src'},
    entry_points = {
        'console_scripts': [
            'WHOSpeeches = WHOSpeeches.__main__:main'
        ],
    },
    classifiers = [        
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic'
    ],
    python_requires = '>=3.10, <4',
    install_requires = [
        "jsonlines>=1.2.0,<2.0.0",
        "lxml>=4.5.0,<5.0.0",
        "nltk>=3.4.5,<4.0.0",
        "progressbar2>=3.51.4,<4.0.0",
        "protego>=0.1.16,<0.2.0",
        "requests>=2.23.0,<3.0.0",
        "requests-cache>=0.9.3,<1.0.0",
        "typeguard>=2.7.1,<3.0.0"],
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'egg_info': CustomEggInfoCommand,
    }
)

#import nltk
#nltk.download('punkt')




