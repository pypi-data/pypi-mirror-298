from setuptools import setup, find_packages

setup(
    name="rf_quick_dashboard",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "plotly",
        "lxml",
    ],
    entry_points={
        "console_scripts": [
            "run_dashboard=error_report.error_report:main",
        ],
    },
    author="Chandan Mishra",
    author_email="testautomasi@gmail.com",
    description="A package to generate a simple html dashboard report for Robot Framework using junit xml output",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
