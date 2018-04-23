# dada


### 安装Nginx
1.安装 brew
``` shell
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"

ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
 ```
 2.安装nginx
 ```shell
    brew install nginx
 ```
 3.启动nginx
 ```shell
    sudo nginx
 ```
 打开查看是否启动：http://localhost:8080/



### 安装python虚拟环境

 1.安装virtualenv
 ```shell
 pip3.5 install virtualenv
 ```
 2.新建虚拟环境文件夹
 ```shell
 mkdir /Users/tian/Library/venv
 cd /Users/tian/Library/venv
 ```
 3.在新建的venv文件夹下:
 ```shell
 which python3   查看python3安装目录
 virtualenv venv --python=python3.5
 ```
 4.进入虚拟环境，安装flask
 ```shell
 source venv/bin/activate
 pip3.5 install flask
 ```

 5.flask文件目录结构：
 ```
 dada_flask
    --static
    --templates
    --start_server.py
    --uwsgi.ini
 ```

### 安装uwsgi
 1.虚拟环境下
 ```shell
 pip3.5 install uwsgi
 ```
 2.在工程目录(就是dada_flask)创建uwsgi.ini(可以将其权限设置为777 sudo chmod 777 uwsgi.ini)
 ```xml
 [uwsgi]
http = 127.0.0.1:8000
processes = 4
threads = 2
master = true
module = start_server  # 写有app的python文件名
pythonpath = /Users/tian/PycharmProjects/dada_flask/
virtualenv = /Users/tian/Library/venv/venv/
callable = app
memory-report = true
wsgi-disable-file-wrapper = true
 ```

### 配置Nginx
 1.查看nginx配置文件路径。
 ```shell
 nginx -V

 结果为：--conf-path=/usr/local/etc/nginx/nginx.conf
 ```
 修改为:
 ```
 http {
    server {
        listen       80;
        server_name  localhost;

        location / {
            include uwsgi_params;
            uwsgi_pass  127.0.0.1:8000;
        }
    }
}

events {
  worker_connections  1024;  ## Default: 1024
}
 ```
 进入nginx安装目录重启nginx
 ```shell
 cd /usr/local/Cellar/nginx/1.13.12/bin
 sudo  ./nginx -s reload
 ```

### 简化启动服务命令

 sudo vim ~/.bash_profile

  1.进入虚拟环境命令:cd-venv
 ```
  alias cd-venv="source /Users/tian/Library/venv/venv/bin/activate"
 ```

 2.开启uwsgi服务器 start_uwsgi
 ```
 alias start_uwsgi="source /Users/tian/Library/venv/venv/bin/activate && cd /    Users/tian/PycharmProjects/dada_flask&&uwsgi --ini uwsgi.ini"
 ```

 3.执行
 ```
 sudo source ~/.bash_profile
 ```

 以后开启服务器就可以直接start_uwsgi
 http://127.0.0.1:8000/