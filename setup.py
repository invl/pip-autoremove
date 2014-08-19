from setuptools import setup

import pip_autoremove


setup(
    name="pip-autoremove",
    version=pip_autoremove.__version__,
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
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
