from setuptools import setup, find_packages

setup(
    name="promptiva",
    version="0.1.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'promptiva=promptiva.cli:main',
        ],
    },
    install_requires=[
        'requests'
    ],
    author="Mahendra Naik",
    author_email="m@promptiva.app",
    description="A tool to work with Promptiva on the cli",
    long_description="This package provides a command-line tool to work with the Promptiva API.",
    long_description_content_type="text/markdown",
    url="https://promptiva.app",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)