from setuptools import find_packages, setup

setup(
    name="dagster_web_etl",
    packages=find_packages(exclude=["dagster_web_etl_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "sqlalchemy",
        "psycopg2-binary",
        "pandas"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
