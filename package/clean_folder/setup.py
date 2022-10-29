from setuptools import setup, find_packages


setup(
    name="clean_folder",
    version="0.0.1",
    autor="Vladislav Tumoschuk",
    entry_points={
        "console_scripts": ["clean-folder=clean_folder.sort:func_path"],
    },
    packages=find_packages(),
    include_package_data=True,
    description="Clean and sort folder script"
)