import markdown2
import secrets

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from markdown2 import Markdown
from . import util

class NewForm(forms.Form):
    title = forms.CharField(label="Title Name", widget=forms.TextInput(attrs={'class': 'form-control col-md-6'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8', 'rows': 5}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    markDown = Markdown()
    entryName = util.get_entry(name)
    if entryName is None:
        return render(request, "encyclopedia/notFound.html", {
            "entry": name
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markDown.convert(entryName),
            "title": name
        })

def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'name': title}))
            else:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "existing": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form,
                "existing": False
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewForm(),
            "existing": False
        })
            

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/notFound.html", {
            "entry": entry
        })
    else:
        form = NewForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/new.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "title": form.fields["title"].initial
        })

def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'name': randomEntry}))

def search(request):
    entry = request.GET.get('q','')
    if util.get_entry(entry) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'name': entry}))
    else:
        entries = []
        for entryName in util.list_entries():
            if entry.upper() in entryName.upper():
                entries.append(entryName)
        
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "search": True,
            "value": entry
        })