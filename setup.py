from setuptools import setup

setup(
    name='decision_house',
    version='0.1',
    description='Help people make decisions about what house they want',
    author='Yang Liu',
    author_email='yangliu3456@gmail.com',
    packages=['src'],
    install_requires=[
        'typer',
        'requests_cache',
        'python-dotenv',
        'pydantic',
        'loguru',
        'pandas',
    ],
)
