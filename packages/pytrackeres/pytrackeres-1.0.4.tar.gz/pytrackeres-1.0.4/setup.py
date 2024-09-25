from setuptools import setup, find_packages

setup(
    name="pytrackeres",
    version="1.0.4",
    author="abutrag",
    author_email="a.butragueno@eulerian.com",
    description="Herramienta para la generación de URLs de tracking en Eulerian.",
    long_description="Herramienta para la generación de URLs de tracking de Eulerian para varios canales de marketing.",
    long_description_content_type="text/markdown",
    url="https://github.com/abutrag/pytrackeres",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pytrackeres=main:main",
        ],
    },
)