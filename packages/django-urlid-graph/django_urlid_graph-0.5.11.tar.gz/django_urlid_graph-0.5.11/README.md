# django-urlid-graph

Django-based API to serve URLid + graph database.
This repository hosts the app code and also a project structure so it's easier
to develop - only the `urlid_graph` folder is packaged before [going to
PyPI](https://pypi.org/project/django-urlid-graph).


## Installation and configuration

1. Add "urlid_graph" to your `INSTALLED_APPS` setting like this:

```python
INSTALLED_APPS = [
    ...
    "urlid_graph",
]
```

2. Change database configurations (this example uses
   [python-decouple](https://github.com/henriquebastos/python-decouple)):

```python
DATABASE_URL = config("DATABASE_URL")  # must be set
GRAPH_DATABASE_URL = config("GRAPH_DATABASE_URL")  # must be set
graph_config = config("GRAPH_DATABASE_URL", cast=db_url)
GRAPH_DATABASE = graph_config["NAME"]  # must be set
DATABASES = {
    "default": config("DATABASE_URL", cast=db_url),
    GRAPH_DATABASE: graph_config,  # must set this way
}
DATABASE_ROUTERS = ["urlid_graph.db_router.RelationAndGraphDBRouter"]
```

3. Configure Django caching system (used to store `ElementConfig` labels):

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 24 * 3600,
        "MAX_ENTRIES": 1024,
    }
}
```

4. Include the `urlid_graph` URLconf in your project's `urls.py` like this:

```python
    path('v1/', include("urlid_graph.urls")),
```

5. Run `python manage.py migrate` to create the needed models, triggers etc.

6. Populate the database:

```shell
# you may want to add entities to urlid_graph_entity model
python manage.py import_config data/config.csv  # must create this file before
python manage.py import_config data/config.csv  # must create this file before
python manage.py import_objects appname Model file.csv.xz  # must create model
python manage.py import_relationships relname file.csv.xz
```


## Importing data

```shell
python manage.py import_objects appname Model file.csv[.gz|.xz]
python manage.py import_relationship relname file.csv[.gz|.xz]
```
