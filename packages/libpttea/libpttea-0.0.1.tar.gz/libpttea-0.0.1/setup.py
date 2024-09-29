import setuptools

with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()
    
setuptools.setup(
    name = "libpttea",
    version = "0.0.1",
    author = "vHrqO",
    author_email="author@example.com",
    description="A Python library that encapsulates various PTT functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bubble-tea-project/libpttea",                                         
    packages=setuptools.find_packages(),     
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
    )