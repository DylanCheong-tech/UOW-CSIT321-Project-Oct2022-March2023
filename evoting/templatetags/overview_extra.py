from django import template

register = template.Library()

@register.filter
def concat_period(event, columntype):
    if columntype == "date":
        return f"{event.startDate} \n to \n {event.endDate}"
    else:
        return f"{event.startTime} \n to \n {event.endTime}"
