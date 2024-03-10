from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

import os

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry's Title")
    content = forms.CharField(widget=forms.Textarea)


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
    entry = util.get_entry(title)

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": util.get_entry(title)
        })
    
    return render(request, "encyclopedia/404.html")


def add(request):
    entries = util.list_entries()

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            
            if title in entries:
                return HttpResponseBadRequest("<h1>The entry already exists.</h1>")

            content = form.cleaned_data.get("content")
            with open(f"C:\\Programming\\CS50 projects\\wiki\\entries\\{title}.md", "w") as f:
                f.write(content)

    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })