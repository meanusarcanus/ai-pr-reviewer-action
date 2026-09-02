from setuptools import setup, find_packages

setup(
    name="pr-agent-pro",
    version="1.0.0",
    description="Automated AI Pull Request Reviewer & Security Code Audit Engine.",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    author="Meanus Arcanus",
    author_email="meanusarcanus@gmail.com",
    url="https://github.com/meanusarcanus/ai-pr-reviewer-action",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
