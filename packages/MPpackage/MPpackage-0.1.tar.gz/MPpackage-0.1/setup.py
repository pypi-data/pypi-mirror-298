from setuptools import setup, find_packages

setup(
    name="MPpackage",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,  # Bao gồm các file không phải Python như .pyd
    package_data={'MPpackage': ['Robot.cp311-win_amd64.pyd']},  # Đảm bảo rằng file .pyd được bao gồm
    description="My custom Python package with a .pyd file",
    author="MP",
    author_email="thuholinh5@gmail.com",
    url="https://github.com/thuholinh5/mypackage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
)
