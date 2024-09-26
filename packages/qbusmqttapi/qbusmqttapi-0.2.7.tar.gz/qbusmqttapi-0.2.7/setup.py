from pathlib import Path

import setuptools

VERSION = "0.2.7"  # PEP-440

setuptools.setup(
    name="qbusmqttapi",
    version=VERSION,
    description="MQTT API for Qbus Home Automation.",
    url="https://github.com/Qbus-iot/qbusmqttapi",
    project_urls={
        "Source Code": "https://github.com/Qbus-iot/qbusmqttapi",
    },
    author="Koen Schockaert",
    author_email="ks@qbus.be",
    license="MIT License 2024",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    # Requirements
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
)