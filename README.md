# bible.drevle.com
API для Острожской Библии

## Установка
Сначала устанавливаем окружение:
```
sudo apt update 
sudo apt install git-core python3-setuptools python3-virtualenv \
    python3-pip python-virtualenv postgresql-9.4 postgresql-client-9.4 \
    postgresql-contrib libpq-dev python3-dev
```

```
git clone git://github.com/vechnoe/bible_drevle_com
cd bible_drevle_com
make
```

## Использование в режиме разработки:
```
make run
```
API будет доступно на: [http://localhost:6543/api/v1/books](http://localhost:6543/api/v1/books)
