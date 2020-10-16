from feed.models import Hashtag
from django.shortcuts import get_object_or_404
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def hashtag_link(content):
    words = content.split()
    result = ''
    print(words)
    for word in words:
        if word.startswith('#'):
            hashtag = get_object_or_404(Hashtag, content = word) 
            word = '<a href="/feed/{}/hashtag/">'.format(hashtag.pk) + word + '</a>'
        elif '#' in word:
            newword = ''
            small_word = ''
            has = 0 
            for str in word:

                if str == '#':
                    has =1 
                    small_word += str
                else: 
                    if has == 0:
                        newword += str 
                    else:
                        if str != '<':
                            small_word += str
                        else: 
                            hashtag = get_object_or_404(Hashtag, content = small_word) 
                            small_word = '<a href="/feed/{}/hashtag/">'.format(hashtag.pk) + small_word + '</a>'
                            newword += small_word + str 
                            has = 0

            if has ==1: 
                hashtag = get_object_or_404(Hashtag, content = small_word) 
                small_word = '<a href="/feed/{}/hashtag/">'.format(hashtag.pk) + small_word + '</a>' 
                newword += small_word
            word = newword

                

        result += word + ' '
    
    result = mark_safe(result)
    return result

