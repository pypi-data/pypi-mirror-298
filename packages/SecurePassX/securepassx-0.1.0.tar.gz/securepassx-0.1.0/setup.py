from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='SecurePassX',
    version='0.1.0',
    py_modules=['SecurePassX'],
    install_requires= ["cryptography==43.0.1", "pytest==8.3.3", "typer==0.12.5", "typing_extensions==4.12.2"],
    packages=find_packages(),
    author='Anurag',
    author_email='kvanurag39@gmail.com',
    entry_points={
        'console_scripts': [
            'SecurePassX=SecurePassX.__main__:main',  # Command to execute your main() function
        ],
    },
    description="A secure password management solution",
    long_description=long_description,
    long_description_content_type="text/markdown",
)