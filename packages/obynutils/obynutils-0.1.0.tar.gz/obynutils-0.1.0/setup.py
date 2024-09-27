from setuptools import setup, find_packages

setup(
    name="obynutils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "disnake",
        "redis",
        "SQLAlchemy",
        "asyncpg",
        "quart",
        "quart-cors",
    ],
    description="A set of utility functions for Obyn bots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="GizmoShiba",
    author_email="gizmoshiba@gmail.com",
    url="https://github.com/gizmoshiba/obyn-utils",
    classifiers=[],
    python_requires=">=3.8",
)
