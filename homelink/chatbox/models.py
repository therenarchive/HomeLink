from django.db import models
from django.contrib.auth.models import User

from service.models import Work

class Conversation(models.Model):
    work = models.ForeignKey(Work, related_name='chatbox', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='chatbox')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)

class ConversationMessages(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


              