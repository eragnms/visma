from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
]

setup(
    name='visma',
    version='0.0.1.dev1',
    description="A Python Client library for integration to Visma e-Accounting, Visma e-Ekonomi",
    long_description=readme + '\n\n' + history,
    author="Henrik Palmlund Wahlgren @ Palmlund Wahlgren Innovative Technology AB",
    author_email='henrik@pwit.se',
    url='https://github.com/pwitab/visma',
    packages=[
        'visma',
    ],

    include_package_data=True,
    install_requires=requirements,

    license="BSD-3",
    zip_safe=False,
    keywords=[],
    classifiers=[

    ],
)