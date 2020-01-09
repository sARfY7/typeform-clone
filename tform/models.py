from django.db import models
from django.conf import settings
from django.utils import timezone
from itertools import chain

# Create your models here.

class Form(models.Model):
    title = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    published_on = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    def publish(self):
        self.published_on = timezone.now()
        self.save()

    def get_order(self):
       text_field_count = len(self.textfield_set.all())
       mcq_field_count = len(self.mcqfield_set.all())
       return text_field_count + mcq_field_count

    def get_fields(self):
        text_fields = self.textfield_set.all()
        mcq_fields = self.mcqfield_set.all()
        fields = chain(text_fields, mcq_fields)
        return sorted(fields, key=lambda x: x.order)

    def __str__(self):
        return f"{self.title}"

class FormResponse(models.Model):
    submitted_on = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey(Form, models.CASCADE)

class TextField(models.Model):
    question = models.TextField()
    order = models.IntegerField()
    form = models.ForeignKey(Form, models.CASCADE)

    def __str__(self):
        return f"(Q: {self.question}) (O :{self.order})"

class TextFieldResponse(models.Model):
    response = models.TextField()
    text_field = models.ForeignKey(TextField, models.CASCADE)
    form_response = models.ForeignKey(FormResponse, models.CASCADE)

    def __str__(self):
        return f"{self.response}"

class McqField(models.Model):
    question = models.TextField()
    order = models.IntegerField()
    form = models.ForeignKey(Form, models.CASCADE)

    def __str__(self):
        return f"(Q: {self.question}) (O :{self.order})"

class McqChoiceField(models.Model):
    text = models.CharField(max_length=100)
    mcq_field = models.ForeignKey(McqField, models.CASCADE)

    def __str__(self):
        return f"{self.text}"

class McqFieldResponse(models.Model):
    mcq_choice_field = models.ForeignKey(McqChoiceField, models.CASCADE)
    mcq_field = models.ForeignKey(McqField, models.CASCADE)
    form_response = models.ForeignKey(FormResponse, models.CASCADE)

    def __str__(self):
        return f"{self.mcq_choice_field}"
