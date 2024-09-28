from setuptools import setup,find_packages

with open('README.md','r',encoding='utf-8') as f:
    long = f.read()

setup(
    name='pi_calculater',
    version='2024.9.28',
    author='LightingLong',
    author_email='17818883308@139.com',
    description='计算π的库',
    long_description=long,
    long_description_content_type='text/markdown',
    url='https://github.com/longliangzhe/pi_calculater',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9'
)