from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from markdown2 import markdown

from random import choice

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry's Title")
    content = forms.CharField(widget=forms.Textarea)

class UpdateEntryForm(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput()) 
    content = forms.CharField(widget=forms.Textarea())


def index(request):
    entries = util.list_entries()
    search = request.GET.get("q")

    if search:
        if search in entries:
            return HttpResponseRedirect(reverse("entry", kwargs={"title": search}))
        entries = [entry for entry in entries if search.lower() in entry.lower()]

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def entry(request, title):
    entry = markdown(util.get_entry(title))

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry,
        })
    
    return render(request, "encyclopedia/404.html")


def random_entry(request):
    entries = util.list_entries()
    title = choice(entries)
    entry = markdown(util.get_entry(title))

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })


def add(request):
    entries = util.list_entries()

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data.get("content")
            
            if title in entries:
                return HttpResponseBadRequest("<h1>The entry already exists.</h1>")

            util.save_or_update_entry(title, content)

            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm(),
    })


def update(request, title):
    entry = util.get_entry(title)

    if request.method == "POST":
        form = UpdateEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")

            util.save_or_update_entry(title, content.replace('\r\n', '\n'))

            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    return render(request, "encyclopedia/update.html", {
        "form": UpdateEntryForm(initial={"title": title, "content": entry}),
        "title": title,
    })
