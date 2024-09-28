from setuptools import setup, find_packages

setup(
    name="solar-as-judge",
    version="0.3.0",
    description="A tool for using SOLAR as a judge in coding competitions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hunkim/solar-as-judge",
    author="Sung Kim",
    author_email="hunkim@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="solar judge coding competition ai",
    packages=find_packages(exclude=["tests", "docs"]),
    install_requires=[
        "langchain>=0.3.0",
        "langchain-upstage>=0.3.0",
    ],
    python_requires=">=3.7",
)
