import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess as sp
from macrolibs.filemacros import get_script_dir


class InstallCommand(install):
    def run(self):
        # Call the original install code
        install.run(self)

        # Run your custom Python script
        script_path = os.path.join(os.path.dirname(__file__), 'pytools4windows', 'pt4winstaller', 'pt4winstaller.py')
        sp.check_call(['python', script_path])


setup(
    name="pytools4windows",
    version="0.1.15",
    packages=find_packages(),
    include_package_data=True,
    author="Casey Litmer",
    author_email="litmerc@msn.com",
    description="Command line tools for Windows",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Casey-Litmer/PyTools4Windows",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "macrolibs",
        "menucmd"
    ],
    package_data= {
        "pytools4windows":["*/__include__.txt",
                           "commandmenu/jsons/*"],
    },
    #entry_points={
    #    'console_scripts': [
    #        'post_install=pytools4windows.pt4winstaller:main',  # Entry point to run the script
    #    ]
    #},
    python_requires='>=3.6',
)
