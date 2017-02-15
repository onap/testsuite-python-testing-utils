from setuptools import setup

setup(
    name='python-openecomp-eteutils',            # This is the name of your PyPI-package.
    version='0.2',                          # Update the version number for new releases     
    description='Scripts written to be used during ete testing',    # Info about script
    install_requires=['dnspython','paramiko', 'pyyaml', 'robotframework', 'deepdiff'], # what we need
    packages=['eteutils'],       # The name of your scipts package
    package_dir={'eteutils': 'eteutils'} # The location of your scipts package
)