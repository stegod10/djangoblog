from django.contrib.auth.views import logout
from django.http import Http404
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import CommentForm

from website import settings
from .models import Category, Post, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
# Class based çalışma içinde class based dosyalar
from django.views.generic.edit import CreateView,UpdateView,DeleteView


from django.contrib import messages

# Anasayfa fonksiyonu
def home_view(request):
    try:
        allCategories = Category.objects.all()
        allPosts = Post.objects.all().order_by('-id')
        paginator = Paginator(allPosts, 2)
        page = request.GET.get('page')
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        return render(request, 'blog/home.html', {
            'categories': allCategories,
            'posts': post,
        })
    except Post.DoesNotExist:
        raise Http404("No MyModel matches the given query.")

# Giriş işlemlerinin yapıldığı kısım
def login_view(request):
    if request.method == "POST" and request.user.is_active != True:
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        if username == "" or password == "":
            context = {
                "login_durum": "Boş alan bırakmayınız."
            }
            return render(request, 'blog/login.html', context)
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                context = {
                    "login_durum": "Bir şeyler yanlış girildi."
                }
                return render(request, 'blog/login.html', context)
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return render(request, 'blog/login.html')

#Category detay sayfası
def category_view(request, slug):
    allCategories = Category.objects.all()
    postAll = Post.objects.filter(category__categorySlug=slug).order_by('-id')

    if not postAll:
        return redirect('/')

    try:
        paginator = Paginator(postAll, 2)
        page = request.GET.get('page')
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'categories': allCategories,
    }
    return render(request, 'blog/category.html', context)

# Makale detay sayfası
def detail_view(request, slug):
    allCategories = Category.objects.all()
    post = get_object_or_404(Post,slug=slug)
    commentsAll = Comments.objects.filter(postInformation=post.id,commentsAllow=1).order_by('-id')
    commentForm = CommentForm(request.POST or None)
    if request.method == 'POST':
        if commentForm.is_valid():
            commentokay = commentForm.save(commit=False)
            commentokay.postInformation = post
            commentokay.ip = request.META['REMOTE_ADDR']
            if request.user.is_authenticated:
                commentokay.nameSurname = request.user.username
                commentokay.email = request.user.email
                commentokay.commentsAllow= 1
            commentokay.save()
            if request.user.is_authenticated:
                messages.success(request, "Yorumunuz başarıyla sisteme eklendi.")
            else:
                messages.success(request, "Yorumunuz yönetime gönderildi ve onay beklemektedir.")
            return redirect(reverse('blog:detail', kwargs={'slug':slug}))
        else:
            messages.warning(request, "Lütfen tüm alanları eksiksiz doldurunuz.")
            commentForm = CommentForm()

    # Okunma sayısını bir arttır.
    post.contentCount = post.contentCount + 1
    post.save()

    context = {
        'post': post,
        'categories': allCategories,
        'commentsAll':commentsAll,
        'commentForm':commentForm,
    }
    return render(request, 'blog/detail.html', context)

# Sistem çıkış işlemi
def logout_view(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    else:
        logout(request)
        return redirect('/')

# Class based view çalışma alanı
# Post ekleme
class PostCreate(CreateView):
    model = Post
    fields = ['title','content','image','category']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.title.replace('ı','i'))
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'slug':self.object.slug})

# Post güncelleme
class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category']
    template_name = 'blog/edit_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.title.replace('ı', 'i'))
        return super(PostUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'slug': self.object.slug})

# Post silme
class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
