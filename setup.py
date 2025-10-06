from setuptools import setup, find_packages

setup(
    name="rollback-multiverse",
    version="0.1.0",
    description="Quantum-inspired branching and collapse for speculative futures",
    author="Research Team",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "pytest>=6.2.0",
    ],
    extras_require={
        "dev": ["pytest>=6.2.0", "black", "flake8"],
    },
)
