from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    categoryName = models.CharField(blank=False, max_length=120,verbose_name="Kategori Adı")
    categorySlug = models.SlugField(unique=True, blank=False)

    def get_absolute_url(self):
        return reverse('blog:category',kwargs={'slug': self.categorySlug})

    def __str__(self):
        return self.categoryName

# Create your models here.
class Post(models.Model):
    blank = True
    null = True
    title = models.CharField(max_length=120,verbose_name="Başlık",blank=False)
    content = models.TextField(blank=False,verbose_name="İçerik")
    date = models.DateTimeField(auto_now_add = True, verbose_name="Yayımlanma Tarihi")
    image = models.ImageField(blank=False)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="postcategory")
    user = models.ForeignKey(User)
    contentCount = models.IntegerField(blank=False,verbose_name="Haber Okundu Sayısı",default=0)

    def __str__(self):
        return self.title

    def get_posts_detail_url(self):
        return reverse('blog:detail', kwargs={'slug':self.slug})

    def get_posts_edit_url(self):
        return reverse('blog:edit', kwargs={'slug': self.slug})

class Comments(models.Model):
    blank = True
    null = True
    COMMENTS_CHOICES = (
        (0, "Hayır"),
        (1, "Evet"),
    )
    email = models.CharField(verbose_name="E-Mail Adresi",blank=False,max_length=300)
    nameSurname = models.CharField(verbose_name="İsim Soyisim",blank=False,max_length=100)
    comments = models.TextField(blank=False,verbose_name="Yorum")
    ip = models.GenericIPAddressField(blank=True,null=True)
    postInformation = models.ForeignKey(Post,related_name="postcomment",blank=True,null=True)
    date = models.DateTimeField(auto_now_add = True, verbose_name="Yayımlanma Tarihi")
    commentsAllow = models.IntegerField(choices=COMMENTS_CHOICES,default=0,blank=False,verbose_name="Yorum Yayın")
    def __str__(self):
        return self.nameSurname

