from django import template

register = template.Library()

@register.filter
def concat_period(event, columntype):
    if columntype == "date":
        return f"{event.startDate} \n to \n {event.endDate}"
    else:
        return f"{event.startTime} \n to \n {event.endTime}"

@register.filter
def status_abbreviation(event):
    status = event.status
    if status == 'PC':
        return "Pending Confirmation"
    elif status == 'PB':
        return "Published"
    elif status == 'VC':
        return "Voting Concluded"
    elif status == 'FR':
        return "Final Result Ready"
    elif status == 'RP':
        return "Result Publish"
    elif status == 'CF':
        return "Confirmation Failed"
