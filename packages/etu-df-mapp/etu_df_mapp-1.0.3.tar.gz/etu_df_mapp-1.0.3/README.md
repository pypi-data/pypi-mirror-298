# 概括
    etu 系列（easy to use）
    让技术更容易使用！
    EDFM脚手架工具(Etu Django Frame Monolithic Application)是在开源Django框架的基础上封装而成，
    以更快捷简便的命令方式，快速创建项目工程，以方便开发使用。次脚手架主要创建Django单体应用，前后端混合，
    前端使用Django模板语法+Layui技术栈。
    

## 说明
    本包名字为 etu-df-mapp , 它主要是EDFM脚手架工具的封装。
    其中支持的Django框架版本：
        4.2.16


### 打包方法
    1. 将要打包的代码文件，统一放在一个目录中，目录名就是pip包的名字；
    2. 在目录外创建一个setup.py文件，并配置好；
    3. 执行 python setup.py sdist命令，完成打包；
    4. 完成打包后，便可通过 pip install 命令进行安装。

### 安装方法
    通过pip命令进行安装：pip install etu-df-mapp
   

### 参数说明
```shell
usage: edfm-admin label project_name
labels:
    4.2.16
```


### 使用方法
```shell
cd ~
edfm-admin 4.2.16 demo_01
```


### 错误反馈