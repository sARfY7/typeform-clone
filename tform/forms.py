from django.forms import ModelForm, CharField
from .models import Form, TextField, McqField, McqChoiceField

class TFormForm(ModelForm):
    class Meta:
        model = Form
        fields = ['title']


class TextFieldForm(ModelForm):
    class Meta:
        model = TextField
        fields = ['question']


class McqFieldForm(ModelForm):
    class Meta:
        model = McqField
        fields = ['question']

class McqChoiceFieldForm(ModelForm):
    class Meta:
        model = McqChoiceField
        fields = ['text']
