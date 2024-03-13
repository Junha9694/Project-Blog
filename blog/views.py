
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Tag
from .forms import CommentForm, PostForm


def blog_list(request):
    # 검색 q가 있을 경우 title과 content에서 해당 내용이 있는지 검색
    q = request.GET.get("q", "")
    if q:
        posts = Post.objects.filter(title__contains=q) | Post.objects.filter(
            content__contains=q
        )
        return render(request, "blog/blog_list.html", {"posts": posts, "q": q})
    posts = Post.objects.all()
    return render(request, "blog/blog_list.html", {"posts": posts})



def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            message = form.cleaned_data["message"]
            c = Comment.objects.create(author=author, message=message, post=post)
            c.save()
    if request.method == "GET": # count 수정
        post.view_count += 1
        post.save()
    return render(request, "blog/blog_detail.html", {"post": post, "form": form})



@login_required
def blog_create(request):
    if request.method == "GET":
        form = PostForm()
        context = {"form": form}
        return render(request, "blog/blog_create.html", context)
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m() 
            return redirect("blog_list")
        else:
            print(form.errors) 
            context = {"form": form}
            return render(request, "blog/blog_create.html", context)

@login_required
def blog_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 내가 쓴 게시물만 업데이트 가능
    if post.author != request.user:
        return redirect("blog_list")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
        context = {"form": form, "pk": pk}
        return render(request, "blog/blog_update.html", context)


@login_required
def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 내가 쓴 게시물만 삭제 가능
    if post.author != request.user:
        return redirect("blog_list")

    if request.method == "POST":
        post.delete()
    return redirect("blog_list")


def blog_tag(request, tag):
    posts = Post.objects.filter(tags__name__iexact=tag)
    return render(request, "blog/blog_list.html", {"posts": posts})


def blog_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect("blog_detail", post_pk)