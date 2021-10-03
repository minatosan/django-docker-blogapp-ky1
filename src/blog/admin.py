from django.contrib import admin
from blog.models import Article,Comment,Tag
# Register your models here.

class TagInline(admin.TabularInline):
  model=Article.tags.through

class ArticleAdmin(admin.ModelAdmin):
  inlines=[TagInline]
  exclude=['tags',]

admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag)

