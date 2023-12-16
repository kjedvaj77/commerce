from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Category

class NewListing(forms.Form):
    category_list = Category.objects.all()
    category_choices = [(category.name, category.name) for category in category_list]
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    image = forms.CharField(label="Image URL")
    price = forms.FloatField(label="price")
    option_field = forms.ChoiceField(choices=category_choices, label="Choose a Category")


def index(request):
    all_categories = Category.objects.all()
    if request.method == "POST":
        category = Category.objects.get(name=request.POST['category'])
        items = Listing.objects.filter(sold=False, category=category)
    else:
        items = Listing.objects.filter(sold=False)
    return render(request, "auctions/index.html", {
        "items": items,
        "categories": all_categories
    })


def listing(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


def new_listing(request):
    if request.method == 'POST':
        form = NewListing(request.POST)
        if form.is_valid():
            # Access form data using the cleaned_data dictionary
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            price = form.cleaned_data['price']
            category = Category.objects.get(name=form.cleaned_data['option_field'])
            item = Listing(
                title=title,
                description=description,
                image=image,
                startingPrice=float(price),
                category=category,
                owner=request.user
            )
            item.save()
            return redirect(reverse('new_listing'))
    else:
        return render(request, "auctions/new_listing.html", {
            "form": NewListing
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
