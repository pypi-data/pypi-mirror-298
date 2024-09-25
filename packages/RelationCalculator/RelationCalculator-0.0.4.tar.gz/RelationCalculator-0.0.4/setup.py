import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "RelationCalculator",
    version = "0.0.4",
    author = "sun" ,
    author_email = "2022200814@mail.buct.edu.cn",
    description = "",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "",
    packages = setuptools.find_packages(),
    install_requires=[  # 依赖项列表
        'numpy',
        'matplotlib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)