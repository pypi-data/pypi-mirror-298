import setuptools
import os
FILE_PATH = os.path.dirname(os.path.realpath(__file__))   # 获取当前文件路径
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
requirements_path = os.path.join(FILE_PATH, 'requirements.txt')  # 读取依赖列表用于传入下方 setup 函数
with open(requirements_path) as f:
    requirements = f.read().splitlines()
setuptools.setup(
    name='testPyPi123',  # 库名称，发布到 Pypi 它就是整个项目的名称，可以与包名不一致。
    version='1.1.0',   # 版本号
    author='1123',   # 作者，发布到 Pypi 它会显示
    author_email='cbs3307821258@qq.com',  # 作者邮箱，发布到 Pypi 它会显示
    description='A package to test',  # 摘要，发布到 Pypi 它会作为摘要显示
    long_description=long_description,  # 详细说明，是直接从 README.md 文件读取内容传过来的
    long_description_content_type='text/markdown',  # 详细说明的渲染方式，设置为 markdown
    url='https://github.com/.....',   # 项目的主页链接
    include_package_data=True,   # 项目是否包含静态数据文件
    # 所包含的数据文件声明，这里的意思是包目录中所有 以.csv, .config, .nl, .json 结尾的文件在安装时都要包含，否则安装时会被忽略
    package_data={'': ['*.csv', '*.config', '*.nl', '*.json']},
    packages=setuptools.find_packages(),   # 包列表，这里使用 find_packages 函数自动扫描和识别包名
    install_requires=requirements,   # 依赖包列表，这里是直接从 requirements.txt 文件中读取后传递进来的，在安装本包的时候依赖包会先置安装
    classifiers=[   # 分类，它会显示在 Pypi 项目主页左侧边栏上，可选列表：https://Pypi.org/classifiers/
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6'   # Python 版本限制，不满足版本限制的环境下将无法安装本包
)