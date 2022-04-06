## postgresql配置
```
sudo apt install postgresql postgresql-contrib
```

```
sudo systemctl start postgresql.service
```

以postgres身份登录：
```
sudo -u postgres psql
```


创建一个django_test用户密码也是django_test。然后创建一个django_test的db，指定所有用户为django_test。

```
postgres=# create role django_test;
CREATE ROLE
postgres=# alter role django_test createdb;
ALTER ROLE
postgres=# alter role django_test login;
ALTER ROLE      
postgres=# alter role django_test password 'django_test';
ALTER ROLE
postgres=# CREATE DATABASE django_test WITH owner = django_test;
CREATE DATABASE
postgres=# 
```


## python环境配置

### 配置pyenv
```
apt update
apt upgrade
```


```
apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl \
git
```

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
```


```
pyenv install --list
```

```
pyenv install 3.10.0
```

如果下载太慢手动下载然后复制文件到 `~/.pyenv/cache` 。

```
pyenv global 3.10.0
```

使用指定python版本：

```
pyenv exec python ....
```

### 安装python依赖
安装psycopg2需要确保下面安装了：
```
apt-get install libpq-dev
```






