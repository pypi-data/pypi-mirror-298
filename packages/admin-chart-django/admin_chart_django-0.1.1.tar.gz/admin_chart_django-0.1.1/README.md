Install the Package : pip install admin-chart-django


Add the App to INSTALLED_APPS
INSTALLED_APPS = [

    'chart', 
]


Run Migrations : python manage.py migrate

After above process go admin panel and there is chart in admin panel
add data and after data added there is view_chart click that and see magic.

In model_field write exists field name of select model in model_name to calculate
total sum. If there is more than one model_field you can write using comma(,).
This model_field is optional.
