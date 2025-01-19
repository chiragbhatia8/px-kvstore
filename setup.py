import setuptools

setuptools.setup(
    name="px-kvstore",
    version="0.1.0",
    packages=setuptools.find_packages(),
    package_dir={"": "."},
    include_package_data=True,
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "px-kvstore=main:cli",  # command -> function
        ],
    },
)
