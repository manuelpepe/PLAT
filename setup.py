import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PLAT",
    version="0.1",
    author="Manuel Pepe",
    author_email="manuelpepe-dev@outlook.com.ar",
    description="GAME, PLAT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuelpepe/plat",
    packages=setuptools.find_packages(),
    install_requires=["pygame"],
    entry_points = {
    	"console_scripts": [
        	"plat = plat:main",
    	]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
)