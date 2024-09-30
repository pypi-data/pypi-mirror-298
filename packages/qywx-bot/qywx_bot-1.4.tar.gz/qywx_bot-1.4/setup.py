import setuptools
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="qywx-bot",
    version="1.4",
    author="sun2ot",
    author_email="sun2ot@qq.com",
    description="python sdk for work wechat robots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sun2ot/qywx-bot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ],
    python_requires='>=3',
)