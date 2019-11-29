配置新网站
=========
* 常见痛点：数据库、静态文件、依赖和自定义设置（开发环境和生产环境之间有差异的设置）；
* 解决方法：只有修改了服务器配置，就运行测试用例进行验收；

## 需要安装的包:
* nginx
* Python 3
* Git
* pip
* virtualenv

以Ubuntu为例，可以执行下面的命令安装:
```
sudo apt-get install nginx git python3 python3-pip
sudo pip3 install virtualenv 
```

## 配置Nginx虚拟主机
* 参考nginx.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com

## Upstart任务
* 参考gunicorn-upstart.template.conf
* 把SITENAME替换成所需的域名，例如staging.my-domain.com

## 文件夹结构
假设有用户账户，家目录为/home/username
```
/home/username 
    └─ sites
        └─ SITENAME 
        ├─ database
        ├─ source 
        ├─ static 
        └─ virtualenv
```

## 附：配置和部署

### 配置
* (1) 假设有用户账户和家目录;
* (2) apt-get nginx git python-pip;
* (3) pip install virtualenv;
* (4) 添加 Nginx 虚拟主机配置;
* (5) 添加 Upstart 任务，自动启动 Gunicorn。

### 部署
* (1) 在 ~/sites 中创建目录结构;
* (2) 拉取源码，保存到 source 文件夹中;
* (3) 启用 ../virtualenv 中的虚拟环境;
* (4) pip install -r requirements.txt;
* (5) 执行 manage.py migrate，创建数据库;
* (6) 执行collectstatic命令，收集静态文件;
* (7) 在 settings.py 中设置 DEBUG = False 和 ALLOWED_HOSTS; (8) 重启 Gunicorn;
* (9) 运行功能测试，确保一切正常。