# setup.py

from setuptools import setup, Extension
from Cython.Build import cythonize

# Khai báo module để Cython hóa
extensions = [
    Extension("my_library_vnstock.my_module", ["my_library_vnstock/my_module.pyx"]),
]

# Thiết lập gói
setup(
    name="my_library_vnstock",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library with secret functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/my_library",
    packages=["my_library_vnstock"],
    ext_modules=cythonize(extensions),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
