from setuptools import find_packages, setup

setup(
    name="isar",
    description="Integration and Supervisory control of Autonomous Robots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version="1.0.5",
    author="Equinor ASA",
    author_email="fg_robots@equinor.com",
    url="https://github.com/equinor/isar",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries",
    ],
    include_package_data=True,
    install_requires=[
        "fastapi"
        "fastapi_utilis"
        "uvicorn"
        "PyJWT",
        "PyYAML",
        "Werkzeug",
        "alitra",
        "azure-identity",
        "azure-keyvault-secrets",
        "azure-storage-blob",
        "cryptography",
        "dacite",
        "injector",
        "numpy",
        "python-dotenv",
        "requests",
        "transitions",
    ],
    python_requires=">=3.8",
    tests_require=[
        "pytest",
        "pytest-dotenv",
        "pytest-mock",
        "requests-mock",
    ],
)
