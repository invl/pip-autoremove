from setuptools import setup


setup(
    name="pip-autoremove",
    version="0.2.0",
    description="Remove a package and its unused dependencies",
    long_description=open('README.rst').read(),
    py_modules=["pip_autoremove"],
    license='Apache License 2.0',
    url='https://github.com/invl/pip-autoremove',
    entry_points="""
    [console_scripts]
    pip-autoremove = pip_autoremove:main
    """,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ]
)
