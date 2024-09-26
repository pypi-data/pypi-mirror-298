from setuptools import setup, find_packages

setup(
    name="pretendapi",  # Package name for installation
    version="0.1.1",
    author="claqz",
    author_email="opexclaqz@egmail.com",
    description="An asynchronous wrapper for the Pretend API.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # This finds all packages in the directory
    install_requires=[
        "aiohttp>=3.8.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
