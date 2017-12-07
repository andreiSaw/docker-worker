from setuptools import setup, find_packages

setup(
    name='skygrid-docker-worker',
    version='0.5.3',
    url='https://github.com/skygrid/docker-worker',
    author='Alexander Baranov',
    author_email='sashab1@yandex-team.ru',
    packages=find_packages(),
    description='SkyGrid docker worker',
    install_requires=[
        "lockfile",
        "requests>=2.5.1",
        "docker-py>=1.1.0",
        "six==1.9.0",
        "raven",
        "hep-data-backends",
        "marshmallow",
        "disneylandClient",
        "protobuf",
    ],
    scripts=[
        'scripts/test-descriptor'
    ]
)
