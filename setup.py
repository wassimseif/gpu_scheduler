from setuptools import setup


def read_readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="gpu_scheduler",
    version="0.0.1",
    description="A scheduler for running commands on multiple GPUs.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/wassimseif/",
    author="Wassim Seifeddine",
    author_email="wassim@wassimseifeddine.com",
    packages=["gpu_scheduler"],
    python_requires=">3.8",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={
        "console_scripts": [
            "gpu_scheduler=gpu_scheduler.api:main",
        ],
    },
    zip_safe=False,
)