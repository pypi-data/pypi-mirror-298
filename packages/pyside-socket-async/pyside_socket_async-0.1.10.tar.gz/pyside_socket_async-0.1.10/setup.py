from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyside_socket_async",
    version="0.1.10",
    author="chakcy",
    author_email="947105045@qq.com",
    description="本框架旨在将运行时间较长的方法在一个线程中执行，最后通过插槽将结果返回给界面，其中涉及 socket 的通信，Qt多线程，Qt插槽，以及任务注册的概念。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/cai-xinpenge/pyside_socket_async",
    include_package_data=True,
    packages=(
        find_packages(where=".")
    ),
    package_dir={
        "": ".",
        "pyside_socket_async":"./pyside_socket_async"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12.4',
    install_requires=[   
        "pydantic>=2.9.1",
        "PySide6>=6.7.2",
        "requests>=2.32.3",
    ]
)