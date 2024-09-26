from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name="summer-ai",
    version="0.0.2",
    author="Aidan Wallace",
    author_email="aidanwallacedev@gmail.com",
    license="MIT",
    description="ai cli tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aidan-wallace/summer",
    packages=find_packages(where="src"),
    install_requires=[requirements],
    python_requires=">=3.10",
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        summer=main:main
    """,
)
