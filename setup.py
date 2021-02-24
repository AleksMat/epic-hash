import os
from setuptools import setup, find_packages


def parse_requirements(file):
    required_packages = []
    with open(os.path.join(os.path.dirname(__file__), file)) as req_file:
        for line in req_file:
            if '/' not in line:
                required_packages.append(line.strip())
    return required_packages


setup(
    name='epic-hash',
    python_requires='>=3.6',
    version='0.1.0',
    description='A package for solving Google Hash Code',
    author='AleksMat',
    author_email='matej.aleksandrov@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements('requirements.txt')
)
