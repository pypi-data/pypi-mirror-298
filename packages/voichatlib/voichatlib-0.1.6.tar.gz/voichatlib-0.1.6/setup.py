from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="voichatlib",  # The name of your library
    version="0.1.6",  # Version of your library
    author="Mert Incesu",  # Your name or your organization's name
    author_email="mert.incesu03@gmail.com",  # Your contact email
    description="A Python library for creating virtual assistants using OpenAI and document retrieval",  # Short description of your library
    long_description=long_description,  # Long description (from README.md)
    long_description_content_type="text/markdown",  # Content type of long description
    url="https://github.com/mertincesu/voi_lib.git",  # URL of the project's homepage (GitHub, etc.)
    packages=find_packages(),  # Automatically find packages in the current directory
    install_requires=[  # Dependencies required by your library
        "requests",
        "openai",
        "langchain",
        "langchain_openai",
        "langchain_community",
        "chromadb",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License under which the library is distributed
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
