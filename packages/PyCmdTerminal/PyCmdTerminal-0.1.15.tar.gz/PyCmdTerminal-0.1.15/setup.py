from setuptools import setup, find_packages

with open('README.en.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyCmdTerminal',
    version='0.1.15',
    author='cainiao dong',
    author_email='xunxiangdong@qq.com',
    description='py-terminal integrates local and remote terminal operations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Xg-dong/python-terminal',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[
        'paramiko'
    ],
)
