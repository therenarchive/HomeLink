from django import forms

from .models import Work

INPUT_CLASSES = 'w-full h-10 rounded-lg px-4 mb-5'

class NewWorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('work_title', 'category', 'price', 'description', 'profile_pic','latitude', 'longitude')
        
        widgets = {
            'work_title': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'Category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

class EditWork(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('work_title', 'price', 'description', 'profile_pic')

        widgets = {
            'work_title': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }
