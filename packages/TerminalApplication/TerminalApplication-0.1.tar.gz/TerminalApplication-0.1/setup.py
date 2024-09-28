from setuptools import setup, find_packages

def parse_requirements(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    # Exclude \"dependency install==1.3.5\"
    requirements = [line.strip() for line in lines if 'install==1.3.5' not in line]
    return requirements

setup(
    name='TerminalApplication',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements('BASH/requirements.txt'),
    entry_points={
        'console_scripts': [
            'terminal_application=mAIn_TerminalApplication:main',
        ],
    },
    package_data={
        '': ['BASH/requirements.txt'],
    },
    include_package_data=True,
)
