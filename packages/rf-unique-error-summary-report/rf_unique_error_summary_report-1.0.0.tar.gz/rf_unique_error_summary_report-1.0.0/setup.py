from setuptools import setup, find_packages

setup(
    name="rf_unique_error_summary_report",
    version="1.0.0",  # Incremented version number
    packages=find_packages(),
    py_modules=["error_summary"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "error_report=error_summary:main",
        ],
    },
    author="Chandan Mishra",
    author_email="testautomasi@gmail.com",
    description="A utility to process robot framework junit XML and then create unique error report with error count and latest test name for easy and quick issue analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
