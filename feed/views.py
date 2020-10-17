from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import CommentForm, ArticleForm
from .models import Article, Comment, Hashtag
from django.http import HttpResponseRedirect




# Create your views here.
def index(request):
    articles=Article.objects.order_by('-pk')
    paginator=Paginator(articles,3) # 숫자 -> 한 페이지에 몇개를 보여줄것인지
    page_number=request.GET.get('page')
    articles=paginator.get_page(page_number)
    context={
        'articles':articles
    }
    return render(request, 'feed/index.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST , request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            for word in article.content.split():
                if word.startswith('#'):
                    hashtag, created = Hashtag.objects.get_or_create(content = word)
                    article.hashtags.add(hashtag)
                
                        
            
            return redirect('feed:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'feed/create.html', context)



@require_http_methods(['GET'])
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    commentform = CommentForm()
    comments = article.comment_set.all()
    paginator=Paginator(comments,3) # 숫자 -> 한 페이지에 몇개를 보여줄것인지
    page_number=request.GET.get('page')
    comments=paginator.get_page(page_number)
    context = {
        'commentform': commentform,
        'comments': comments,
        'article': article,
    }
    return render(request, 'feed/detail.html', context)


@require_http_methods(['GET', 'POST'])
def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST': # update
        # Create a form to edit an existing Article, but use
        # POST data to populate the form.
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('feed:detail', article.pk)
    else: # edit
        # Creating a form to change an existing article.
        form = ArticleForm(instance=article)
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'feed/update.html', context)


@require_http_methods(['GET', 'POST'])
def delete(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    if request.method == "POST":
        
        article.delete()
        return redirect('feed:index')
    else:
        context={
            'article': article,
        }
        return render(request,'feed/delete.html',context)


@require_POST
def comments(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        article = get_object_or_404(Article, pk=article_pk)
        if form.is_valid:
            comments = form.save(commit=False)
            comments.user = request.user
            comments.article = article
            comments.save()
            return redirect('feed:detail', article.pk)
        else:
            context = {
                'form': form,
                'article': article,
            }
        return render(request, 'feed/detail.html', context)
    return redirect('account:login')

@require_POST
def like(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article,pk=article_pk)
        if request.user in article.like_users.all():
            article.like_users.remove(request.user)
            liked = False
        else:
            article.like_users.add(request.user)
            liked = True
        like_status = {
            'liked':liked,
            'like_count':article.like_users.count(),
        }
        return JsonResponse(like_status)
    else:
        return redirect('account:login')


def hashtag(request, hashtag_pk):
    tag = get_object_or_404(Hashtag,pk=hashtag_pk)
    articles = tag.tagged_articles.all()
    context = {
        'tag':tag,
        'articles':articles,
    }
    return render(request,'feed/hashtag.html',context)

        