from setuptools import setup, find_packages

setup(
    name="google_drive_id_extractor",
    version="0.1.0",
    packages=find_packages(),
    description="This will extract the Google Drive file ID from any provided Google Drive link, making it easy to retrieve the ID programmatically. It's lightweight, simple to use, and supports various Google Drive link formats.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kazim",
    author_email="kazimshah39@gmail.com",
    url="https://toolsforfree.com/",
    python_requires=">=3.6",
)
