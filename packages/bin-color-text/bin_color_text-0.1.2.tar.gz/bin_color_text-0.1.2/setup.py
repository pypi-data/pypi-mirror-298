from setuptools import setup, find_packages

setup(
    name="bin_color_text",
    version="0.1.2",
    author="caolib",
    author_email="1265501579@qq.com",
    description="A tool for printing colored strings in the terminal",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/caolib/color_text",  # 替换为你的GitHub仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)