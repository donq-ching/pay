# pay
薪酬管理系统

# 导出项目依赖

```bush
pipreqs ./ --encoding=utf8
```

# 安装依赖
```bush
pip install -r requriements.txt
```

# Start

```bush
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 80
```