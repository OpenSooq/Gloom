# <p align="center">Gloom - Opensooq URL shortener</p>

![Goom](/public/assets/images/gloom.png)

Gloom allows you to shorten URLs just as you would on your domain. Users can create these short links through the web interface For example, to shorten the URL http://www.google.com/, access UI admin:

![Goom](/public/new-skin.png)

Put your url then submit, you will see the shortner url.

or they can programatically create them through the Gloom API. With the Gloom API you can write applications that use simple HTTP methods to create short links from desktop, mobile, or web.

## API Doc
```
API : /shorten
Method : POST
Params : longURL
```

For instance, you could issue the following curl command (POST request):

```
curl https://YourDomain/shorten \
  -H 'Content-Type: application/json' \
  -d '{"longUrl": "http://www.google.com/"}'
```
If successful, the response will look like:

```javascript
{ 
  shorten: "XXX",
  link : "XXXXXXX"
}
```
-------------------------------------------------------------------------------------

Links that users create through the Gloom can also open directly in your mobile applications that can handle those links. This automatic behavior provides the best possible experience to your app users who open your domain links, no matter what platform or device they are on.

This project running by [Python](https://www.python.org/) with [MongoDB](https://www.mongodb.com/) as a backend and done using [BottlePy](https://github.com/bottlepy/bottle) and [uPyApp](https://github.com/muayyad-alsadi/uPyApp)

## Installation

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
