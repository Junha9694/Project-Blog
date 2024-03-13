from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "main/index.html")


def blog(request):
    # 검색 q가 있을 경우 title과 content에서 해당 내용이 있는지 검색
    q = request.GET.get("q", "")
    if q:
        posts = Post.objects.filter(title__contains=q) | Post.objects.filter(
            content__contains=q
        )
        return render(request, "blog/blog_list.html", {"posts": posts, "q": q})
    posts = Post.objects.all()
    return render(request, "blog/blog_list.html", {"posts": posts})



def account(request):
    return render(request, "account/profile.html")
