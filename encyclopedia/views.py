from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry's Title")
    content = forms.CharField(label="New Entry")


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
    
