from setuptools import setup, find_packages

setup(
    name="pglogginghandler",
    version="0.1",
    packages=find_packages(),
    install_requires=['psycopg2-binary==2.9.9'],
    description="Simple logging to postgres handler",
    author="Marcus Oates",
    author_email="moates695@gmail.com",
    url="https://github.com/moates695/pglogging",
)
