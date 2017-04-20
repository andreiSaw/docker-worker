from setuptools import setup, find_packages

setup(
    name='skygrid-docker-worker',
    version='0.4.19',
    url='https://github.com/skygrid/docker-worker',
    author='Alexander Baranov',
    author_email='sashab1@yandex-team.ru',
    packages=find_packages(),
    description='SkyGrid docker worker',
    install_requires=[
        "lockfile==0.10.2",
        "requests>=2.5.1",
        "skygrid-libscheduler>=0.5.7",
        "docker-py>=1.1.0",
        "six==1.9.0",
        "websocket-client>=0.26.0",
        "wsgiref==0.1.2",
        "raven",
        "hep-data-backends",
    ],
    scripts = [
        'scripts/test-descriptor'
    ]
)
