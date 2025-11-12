from django import forms

from .models import ConversationMessages

class ConversationMessagesForm(forms.ModelForm):
    class Meta:
        model = ConversationMessages
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full h-10 px-4 py-2 rounded-lg px-4 mb-5 mt-3',
            })
        }