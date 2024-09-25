from setuptools import setup, find_packages

setup(
    name="svc_order_zxw",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.112.0,<0.113',
        'sqlalchemy==2.0.32',
        'greenlet==3.0.3',
        'asyncpg==0.29.0',
        'uvicorn>=0.30.0,<0.31.0',
        'app-tools-zxw>=1.0.80',
    ],
    author="薛伟的小工具",
    author_email="",
    description="订单与支付服务",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunshineinwater/",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
