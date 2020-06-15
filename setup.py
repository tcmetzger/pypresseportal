from setuptools import setup

from pypresseportal import __version__


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="pypresseportal",
    version=__version__,
    description="Python wrapper for the presseportal.de API",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    keywords=[
        "pypresseportal",
        "presseportal",
        "DPA",
        "press release",
        "press releases",
        "police",
        "fire department",
        "news",
        "journalism",
        "Germany",
    ],
    url="https://github.com/tcmetzger/pypresseportal",
    author="Timo Cornelius Metzger",
    author_email="coding@tcmetzger.net",
    license="MIT",
    packages=["pypresseportal"],
    package_dir={"pypresseportal": "pypresseportal"},
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["requests"],
)
