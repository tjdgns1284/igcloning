from feed.models import Hashtag
from django.shortcuts import get_object_or_404
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def hashtag_link(content):
    new_content=''
    for str in content:
        if str =='<':
            new_content += ' ' +str
        elif str == '>':
            new_content +=  str + ' '
        else: 
            new_content+= str

    words = new_content.split()
    result = ''
    print(words)
    for word in words:
        if word.startswith('#'):
            hashtag = get_object_or_404(Hashtag, content = word) 
            word = '<a href="/feed/{}/hashtag/">'.format(hashtag.pk) + word + '</a>'
                       

        result += word + ' '
    
    result = mark_safe(result)
    return result

