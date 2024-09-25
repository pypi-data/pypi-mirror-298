# Welcome to our library | dj-rest-tickets

### dj-rest-tickets  is a library use DRF to give you EndPoints for :
- send tickets with obervers
- follow proccess of resolve tickets
- give admins control
- make communication good into users


## Get started

`pip install dj-rest-tickets`

add to your settings :

```
INSTALLED_APPS = [
    ...,
    'dj_rest_tickets',
    'dj_rest_tickets.tickets',
    'rest_framework', # just for drf api interface
]
```

than add urls :

```
path('tickets/', include('dj_rest_tickets.urls')),
```

### future features:
- mailing
- roles