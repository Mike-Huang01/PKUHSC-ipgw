# PKUHSC-ipgw
* Mike Huang

python脚本，用于登录、登出和注销北医网关

需要：
1. 安装python3.x(https://www.python.org/downloads/)
2. 配置好python的环境变量（windows中`我的电脑`-`控制面板`-`环境变量设置`），将python的安装目录填上
3. 打开命令行， 输入 `pip install httplib2`

登录，登出，注销（选择其中一个参数）
~~~
macos or linux: 
python your_dir/login.py [login|lgout|logout] 

windows:
python x:\your_dir\login.py [login|lgout|logout] 
~~~ 

同目录下会产生登录日志：login_log.txt
配置文件：config.json

