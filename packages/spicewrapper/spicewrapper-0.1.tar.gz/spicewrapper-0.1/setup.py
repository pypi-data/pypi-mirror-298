from setuptools import setup, find_packages

setup(
    name="spicewrapper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "pyperclip",
    ],
    author="jeff chiles",
    author_email="pseudotexan@gmail.com",
    description="Tool to automate running, editing, and plotting NGSpice simulations (preview version)",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/pseudotexan/spicewrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)