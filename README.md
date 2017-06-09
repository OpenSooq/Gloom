# Gloom - Opensooq URL shortener

![Goom](/public/assets/gloom.png)

Gloom allows you to shorten URLs just as you would on your domain. Users can create these short links through the web interface For example, to shorten the URL http://www.google.com/, access UI admin:

<img width="452" alt="Admin" src="https://user-images.githubusercontent.com/4533327/26978058-b275883c-4d32-11e7-8325-a9ac740df428.png">

Put your url then submit, you will see the shortner url.

Links that users create through the URL Shortener can also open directly in your mobile applications that can handle those links. This automatic behavior provides the best possible experience to your app users who open your domain links, no matter what platform or device they are on.

This application was done using [BottlePy](https://github.com/bottlepy/bottle) and [uPyApp](https://github.com/muayyad-alsadi/uPyApp)

## Installation

This project running by Python with MongoDB as a backend

1. You need a domian to use it for shorting URL
2. Install MongoDB
3. You need `pymongo3`

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

## API Doc

Users can create these short links through the web interface or they can programatically create them through the URL Shortener API. With the URL Shortener API you can write applications that use simple HTTP methods to create short links from desktop, mobile, or web.

```
API : /shorten
Method : POST
Params : longURL
```
Resposnse :

```javascript
{ 
  shorten: "XXX",
  link : "XXXXXXX"
}
```

