from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="game_asset_library",  # Unique package name
    version="1.0.0",  # Version number
    author="Your Name",
    author_email="your.email@example.com",
    description="A fully-featured game asset library for Pygame with customizable assets, animations, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourgithubusername/game_asset_library",  # GitHub repo URL (optional)
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
        "numpy>=1.21.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your preferred license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
