from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fastforge",
    version="0.0.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "fastapi",
    ],
    entry_points="""
        [console_scripts]
        fastforge=fastforge.cli:fastforge
    """,
    author="Soham Sagathiya",
    author_email="soham.saga@gmail.com",
    description="A FastAPI utility CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soham901/fastforge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    license="MIT",
)
