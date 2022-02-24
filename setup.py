from setuptools import setup
from src.install import InstallOverride

with open('README.md', 'r') as fp:
    long_description = fp.read()
with open('requirements.txt', 'r') as fp:
    requires = [req.strip() for req in fp.readlines()]

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
    install_requires = requires,
    cmdclass = { 'install': InstallOverride }
)
