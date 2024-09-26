from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read() #这里主要是从readme中读取一下项目的描述

setup(
    name='mt_tts_sdk',  #这过是包名，即打包发布之后 pip install mttts 即可安装
    version='0.0.1',	#版本号
    packages=find_packages(), #这主要是读取一个有__init__.py的目录，也可以自己写[example1,example2]等，不过可以交给setuptools让它去搜索。
    url='https://dev.sankuai.com/code/repo-detail/~ZHANGZHANG05/speechsdk/file/list', #对应项目的git地址
    license='MIT', #该包的授权信息，直接采用的示例。
    author='zhangzhang', #包的作者
    author_email='zhangzhang05@sankuai.com',	#作者的邮箱联系方式
    description='语音服务SDK',	#包的简单描述
    long_description=long_description,	#包的详细描述 由于是从md文件读的描述，所以有下一行
    long_description_content_type="text/markdown",
    install_requires=['requests==2.27.1'],	#安装此包所需要的依赖
    classifiers=[ #包的一些分类信息，方便在pypi上检索
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',	#安装该包的python要求
)