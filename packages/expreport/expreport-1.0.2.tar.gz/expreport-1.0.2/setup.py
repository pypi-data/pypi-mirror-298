from setuptools import find_packages,setup

with open('requirements.txt','r',encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name="expreport",
    version="1.0.2",
    author="Aymen Jemi",
    author_email="jemiaymen@gmail.com",
    description="export data from csv to documents word",
    licence="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "expreport=expreport:cli"
        ]
    },
)
