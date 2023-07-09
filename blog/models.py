from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


from django.db.models import BigAutoField
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""" Post model """
class Post(models.Model):
    title = models.CharField(max_length=150,null=True)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    likes = models.ManyToManyField(User, related_name="blogpost", blank=True,null=True)
    saves = models.ManyToManyField(User, related_name="blogsave", blank=True,null=True)

    def total_likes(self):
        return self.likes.count()

    def total_saves(self):
        return self.saves.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk":self.pk})


""" Comment model """
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments" , on_delete=models.CASCADE,null=True)
    name = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    body = models.TextField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True,null=True)
    likes = models.ManyToManyField(User, related_name="blogcomment", blank=True,null=True)
    reply = models.ForeignKey('self', null=True, related_name="replies", on_delete=models.CASCADE)

    def total_clikes(self):
        return self.likes.count()

    def __str__(self):
        return '%s - %s - %s' %(self.post.title, self.name, self.id)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk":self.pk})

