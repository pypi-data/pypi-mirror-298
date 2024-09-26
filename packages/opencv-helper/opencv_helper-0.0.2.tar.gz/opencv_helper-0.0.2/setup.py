from setuptools import find_packages, setup

NAME = "opencv_helper"
DESCRIPTION = "opencv helper"
URL = ""
EMAIL = "421826878@qq.com"
AUTHOR = "guozi"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.0.2"

REQUIRED = [
    "opencv_python",
    "numpy",
    # 'requests', 'maya', 'records',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description="",
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
