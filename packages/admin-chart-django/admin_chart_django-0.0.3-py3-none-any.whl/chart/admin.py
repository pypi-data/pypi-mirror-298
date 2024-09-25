from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.urls import path
from django.urls import reverse
from django.shortcuts import render
from django.db.models import Count, Sum
from chart.models import Chart
from django.core.exceptions import FieldDoesNotExist

# Register your models here.

@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'view_chart')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chart/<int:chart_id>/', self.admin_site.admin_view(self.chart_view), name='chart_view'),
        ]
        return custom_urls + urls

    def view_chart(self, obj):
        url = reverse('admin:chart_view', args=[obj.id])
        return format_html('<a href="{}">View Chart</a>', url)

    def chart_view(self, request, chart_id):
        chart = Chart.objects.get(id=chart_id)
        model = chart.model_name.model_class()
        model_field = chart.model_field  # Get the dynamic field name(s) from the chart instance

        # Try to use 'date_joined' or 'created_at' for the date grouping
        date_field = None
        try:
            model._meta.get_field('date_joined')
            date_field = 'date_joined'
        except FieldDoesNotExist:
            try:
                model._meta.get_field('created_at')
                date_field = 'created_at'
            except FieldDoesNotExist:
                return render(request, 'admin/chart_template.html', {
                    'chart': chart,
                    'model_name': chart.model_name.name,
                    'model_field': model_field,
                    'error': 'Neither "date_joined" nor "created_at" exists in the model.',
                })

        # Annotate data by the chosen date field
        data = model.objects.values(date_field).annotate(count=Count(date_field)).order_by(date_field)

        datasets = []

        # Check if model_field is provided
        if model_field:
            fields = [field.strip() for field in model_field.split(',')]  # Split by comma and strip whitespace
            # Calculate the total sum per date for each dynamic field
            for field in fields:
                total_sum_data = model.objects.values(date_field).annotate(total_sum=Sum(field)).order_by(date_field)

                # Prepare the total sum values for the field
                total_sum_values = []
                for entry in data:
                    date_str = entry[date_field].strftime('%Y-%m-%d')
                    total_sum_entry = next((item for item in total_sum_data if item[date_field].strftime('%Y-%m-%d') == date_str), None)
                    total_sum_value = total_sum_entry['total_sum'] if total_sum_entry else 0
                    total_sum_values.append(total_sum_value)

                datasets.append({
                    'label': f'Total {field}',
                    'data': total_sum_values,
                    'borderColor': self.get_color_for_dataset(len(datasets)),  # Assign a unique color
                    'borderWidth': 2,
                    'fill': False,
                })
        else:
            # If no model_field is provided, only return counts
            dates = [entry[date_field].strftime('%Y-%m-%d') for entry in data]
            counts = [entry['count'] for entry in data]

        return render(request, 'admin/chart_template.html', {
            'chart': chart,
            'model_name': chart.model_name.name,
            'model_field': model_field,
            'dates': [entry[date_field].strftime('%Y-%m-%d') for entry in data],
            'counts': [entry['count'] for entry in data],
            'datasets': datasets,  # Pass datasets for rendering in template
        })

    def get_color_for_dataset(self, index):
        # List of colors for datasets
        colors = [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
        ]
        return colors[index % len(colors)]  # Cycle through colors