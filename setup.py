from setuptools import setup, find_packages

setup(
    name="esphome-jh-bms-esp32",
    version="1.0.0",
    description="ESPHome component for JH BMS ESP32",
    long_description="ESPHome component for communicating with JH BMS using ESP32",
    author="",
    author_email="",
    license="MIT",
    packages=find_packages(),
    package_data={
        "": ["*.yaml", "*.md", "*.h", "*.cpp"],
    },
    include_package_data=True,
    install_requires=[
        "esphome>=2023.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
    ],
    keywords=["esphome", "bms", "battery management system", "esp32", "jh bms"],
    python_requires=">=3.9",
)