from django.db import models
from django.urls import reverse

# Create your models here.
from accounts.models import CustomUser

class Category(models.Model):
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
    )
    
    def __str__(self):
        return self.title

class StrategyPost(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )
    
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
    )
    
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )
    
    strategy = models.TextField(
        verbose_name='攻略方法',
    )
    
    image1 = models.ImageField(
        verbose_name='イメージ1',
        upload_to='photos'
    )
    
    image2 = models.ImageField(
        verbose_name='イメージ2',
        upload_to='photos',
        blank=True,
        null=True
    )

    image3 = models.ImageField(
        verbose_name='イメージ3',
        upload_to='photos',
        blank=True,
        null=True
    )

    image4 = models.ImageField(
        verbose_name='イメージ4',
        upload_to='photos',
        blank=True,
        null=True
    )
    
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

    def __str__(self):
        return self.title


#----------------------------------------------------------
class Comment(models.Model):
    """記事に紐づくコメント"""
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    text = models.TextField(
        verbose_name='本文'
    )
    target = models.ForeignKey(
        StrategyPost, 
        on_delete=models.CASCADE, 
        verbose_name='対象記事'
    )