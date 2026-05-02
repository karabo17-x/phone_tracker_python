
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phone-tracker",
    version="2.0.0",
    author="Karabo Mothapo",
    description="South African Phone Number Intelligence Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karabo17-x/phone-tracker-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Telephony",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'phone-tracker=phone_tracker.ui.cli:run_cli',
        ],
    },
)
