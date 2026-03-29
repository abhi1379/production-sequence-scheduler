from setuptools import setup, find_packages

setup(
    name="production-sequence-scheduler",
    version="1.0.0",
    description="Production sequence scheduling engine with constraints",
    author="abhi1379",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "ortools>=9.7.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "pytest>=7.4.0",
    ],
)
