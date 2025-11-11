from django import template

register = template.Library()

@register.filter
def get_response(responses, freelancer_id):
    return responses.filter(freelancer__id=freelancer_id).first()
