from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .models import Form, TextField, McqField, McqChoiceField, TextFieldResponse, McqFieldResponse, FormResponse
from .forms import TFormForm, TextFieldForm, McqFieldForm, McqChoiceFieldForm
import json, csv

# Create your views here.

@login_required
def form_list(request):
    forms = Form.objects.filter(user=request.user)
    return render(request, 'tform/form_list.html', {'forms': forms})


def form_view(request, id):
    form = get_object_or_404(Form.objects.prefetch_related(), pk=id)
    if (not form.published_on and (request.user != form.user)):
        raise PermissionDenied
    fields = form.get_fields()
    if request.method == 'POST':
        form_response = FormResponse.objects.create(form=form)
        for form_data_field in request.POST:
            form_data_field_slug = form_data_field.split('-')
            form_data_field_type = form_data_field_slug[0]
            if len(form_data_field_slug) == 2:
                form_data_field_id = form_data_field_slug[1]
            form_data_field_value = request.POST.get(form_data_field)
            if (form_data_field_type == 'text'):
                text_field_response = TextFieldResponse.objects.create(response=form_data_field_value, text_field=TextField.objects.get(pk=form_data_field_id), form_response=form_response)
            if (form_data_field_type == 'mcq'):
                mcq_field_response = McqFieldResponse.objects.create(mcq_choice_field=McqChoiceField.objects.get(pk=form_data_field_value), mcq_field=McqField.objects.get(pk=form_data_field_id), form_response=form_response)
    return render(request, 'tform/form_view.html', {'form': form, 'fields': fields})


@login_required
def form_delete(request, id):
    form = get_object_or_404(Form, pk=id)
    if form.user != request.user:
        raise PermissionDenied
    form.delete()
    return redirect('form_list')


@login_required
def form_publish(request, id):
    form = get_object_or_404(Form.objects.prefetch_related(), pk=id)
    if form.user != request.user:
        raise PermissionDenied
    form.publish()
    return redirect('form_view', id=form.pk)

@login_required
def form_new(request):
    if request.method == 'POST':
        form = TFormForm(request.POST)
        if form.is_valid():
            tform = form.save(commit=False)
            tform.user = request.user
            tform.save()
            return redirect('form_list')
    else:
        form = TFormForm()
    return render(request, 'tform/form_new.html', {'form': form})


@login_required
def form_edit(request, id):
    form = get_object_or_404(Form.objects.prefetch_related('textfield_set', 'mcqfield_set'), pk=id)
    if form.user != request.user:
        raise PermissionDenied
    form_fields = form.get_fields()
    return render(request, 'tform/form_edit.html', {'form': form, 'fields': form_fields})


@login_required
def textfield_new(request, id):
    tform = get_object_or_404(Form, pk=id)
    if tform.user != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = TextFieldForm(request.POST)
        if form.is_valid():
            text_field = form.save(commit=False)
            text_field.order = tform.get_order() + 1
            text_field.form = tform
            text_field.save()
            return redirect('form_edit', id=tform.pk)
    else:
        form = TextFieldForm()
    return render(request, 'tform/textfield_edit.html', {'form': form, 'edit_mode': False})


@login_required
def mcqfield_new(request, id):
    tform = get_object_or_404(Form, pk=id)
    if tform.user != request.user:
        raise PermissionDenied
    McqChoiceFieldFormset = inlineformset_factory(McqField, McqChoiceField, fields=('text',), extra=1, can_delete=True)
    if request.method == 'POST':
        mcq_field_form = McqFieldForm(request.POST)
        formset = McqChoiceFieldFormset(request.POST)
        if mcq_field_form.is_valid():
            new_mcq_field = mcq_field_form.save(commit=False)
            new_mcq_field.form = tform
            new_mcq_field.order = tform.get_order() + 1
            formset = McqChoiceFieldFormset(request.POST, instance=new_mcq_field)

            if formset.is_valid():
                new_mcq_field.save()
                formset.save()
                return redirect('form_edit', id=tform.pk)
    else:
        mcq_field_form = McqFieldForm()
        formset = McqChoiceFieldFormset()
    return render(request, 'tform/mcqfield_edit.html', {'form': mcq_field_form, 'formset': formset})


@login_required
def textfield_edit(request, form_id, id):
    tform = get_object_or_404(Form, pk=form_id)
    if tform.user != request.user:
        raise PermissionDenied
    text_field = get_object_or_404(TextField, pk=id)
    if request.method == 'POST':
        form = TextFieldForm(request.POST, instance=text_field)
        if form.is_valid():
            form.save()
            return redirect('form_edit', id=tform.pk)
    else:
        form = TextFieldForm(instance=text_field)
    return render(request, 'tform/textfield_edit.html', {'form': form, 'edit_mode': True})


@login_required
def mcqfield_edit(request, form_id, id):
    tform = get_object_or_404(Form, pk=form_id)
    if tform.user != request.user:
        raise PermissionDenied
    mcq_field = get_object_or_404(McqField.objects.select_related(), pk=id)
    McqChoiceFieldFormset = inlineformset_factory(McqField, McqChoiceField, fields=('text',), extra=0, can_delete=True)
    if request.method == 'POST':
        mcq_field_form = McqFieldForm(request.POST, instance=mcq_field)
        formset = McqChoiceFieldFormset(request.POST, instance=mcq_field)
        if mcq_field_form.is_valid():
            if formset.is_valid():
                updated_mcq_field = mcq_field_form.save()
                formset.save()
                return redirect('form_edit', id=tform.pk)
    else:
        mcq_field_form = McqFieldForm(instance=mcq_field)
        formset = McqChoiceFieldFormset(instance=mcq_field)
    return render(request, 'tform/mcqfield_edit.html', {'form': mcq_field_form, 'formset': formset})


@login_required
def textfield_delete(request, form_id, id):
    form = get_object_or_404(Form, pk=form_id)
    if form.user != request.user:
        raise PermissionDenied
    text_field = get_object_or_404(TextField, pk=id)
    if form.user == request.user:
        text_field.delete()
    return redirect('form_edit', id=form.pk)


@login_required
def mcqfield_delete(request, form_id, id):
    form = get_object_or_404(Form, pk=form_id)
    if form.user != request.user:
        raise PermissionDenied
    mcq_field = get_object_or_404(McqField, pk=id)
    if form.user == request.user:
        mcq_field.delete()
    return redirect('form_edit', id=form.pk)


@login_required
def response_list(request, id):
    form = get_object_or_404(Form.objects.prefetch_related(), pk=id)
    if form.user != request.user:
        raise PermissionDenied
    responses = form.formresponse_set.all()
    return render(request, 'tform/response_list.html', {'form': form, 'responses': responses})


@login_required
def response_view(request, form_id, id):
    form = get_object_or_404(Form.objects.prefetch_related(), pk=form_id)
    if form.user != request.user:
        raise PermissionDenied
    form_response = get_object_or_404(FormResponse.objects.prefetch_related(), pk=id)
    fields = form.get_fields()
    return render(request, 'tform/response_view.html', {'form': form, 'fields': fields, 'response': form_response})


@login_required
def response_download(request, id):
    form = get_object_or_404(Form.objects.prefetch_related(), pk=id)
    if form.user != request.user:
        raise PermissionDenied
    form_responses = form.formresponse_set.all()
    if len(form_responses) == 0:
        return redirect('response_list', id=form.pk)
    form_fields = form.get_fields()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename='{form.title}-responses.csv'"
    writer = csv.writer(response)
    writer.writerow([field.question for field in form_fields])
    for form_response in form_responses:
        responses = []
        for field in form_fields:
            if type(field) is TextField:
                text_field_response = TextFieldResponse.objects.filter(form_response=form_response, text_field=field).first()
                if text_field_response:
                    responses.append(text_field_response.response)
            if type(field) is McqField:
                mcq_field_response = McqFieldResponse.objects.filter(form_response=form_response, mcq_field=field).first()
                if mcq_field_response:
                    responses.append(mcq_field_response.mcq_choice_field)
        writer.writerow(responses)
    return response


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('form_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
