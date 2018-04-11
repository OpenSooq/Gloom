# Gloom - Opensooq URL shortener

![Goom](/public/assets/images/gloom.png)

This application was done using [BottlePy](https://github.com/bottlepy/bottle) and [uPyApp](https://github.com/muayyad-alsadi/uPyApp)

## Installation

You need `pymongo3`

```
virtualenv --system-site-packages virtualenv
source virtualenv/bin/activate
pip install bottle
```

## Configuration

```
cp example/{uwsgi.ini,app.ini} ./
```

Then edit those two files. For dev env use 

```
cp example/uwsgi-dev.ini ./uwsgi.ini
```

## Setup Database

```
./cli migrate
```


