from django import template

register = template.Library()

@register.filter
def concat_period(event, columntype):
    if columntype == "date":
        return f"{event.startDate} to {event.endDate}"
    else:
        return f"{event.startTime} to {event.endTime}"
