from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Form(models.Model):
    title = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    def publish(self):
        self.published_on = timezone.now()
        self.save()

    def __str__(self):
        return f"<Form {self.title}>"

class FormResponse(models.Model):
    form = models.ForeignKey(Form, models.CASCADE)

class TextField(models.Model):
    question = models.TextField()
    order = models.IntegerField()
    form = models.ForeignKey(Form, models.CASCADE)

    def __str__(self):
        return f"<TextField (Q: {self.question}) (O :{self.order})>"

class TextFieldResponse(models.Model):
    response = models.TextField()
    text_field = models.ForeignKey(TextField, models.CASCADE)
    form_response = models.ForeignKey(FormResponse, models.CASCADE)

    def __str__(self):
        return f"<TextFieldResponse {self.response}>"

class McqField(models.Model):
    question = models.TextField()
    order = models.IntegerField()
    form = models.ForeignKey(Form, models.CASCADE)

    def __str__(self):
        return f"<McqField (Q: {self.question}) (O :{self.order})>"

class McqChoiceField(models.Model):
    text = models.TextField()
    mcq_field = models.ForeignKey(McqField, models.CASCADE)

    def __str__(self):
        return f"<McqChoiceField {self.text}>"

class McqFieldResponse(models.Model):
    mcq_choice_field = models.ForeignKey(McqChoiceField, models.CASCADE)
    mcq_field = models.ForeignKey(McqField, models.CASCADE)
    form_response = models.ForeignKey(FormResponse, models.CASCADE)

    def __str__(self):
        return f"<McqFieldResponse {self.response}>"
