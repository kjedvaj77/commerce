from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bid
from .forms import NewListing, BidForm


def place_bid(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        bids = Bid.objects.filter(auction=listing).order_by('-amount')
        bid_form = BidForm(request.POST)
        if not bid_form.is_valid():
            return redirect(reverse("listing", args=[id]))
        else:
            bid_amount = bid_form.cleaned_data['amount']
            if not bids and bid_amount > listing.startingPrice:
                bid = Bid(bidder=request.user, auction=listing, amount=bid_amount)
                bid.save()
                return redirect(reverse("listing", args=[id]))
            elif bids and bid_amount > bids[0].amount:
                bid = Bid(bidder=request.user, auction=listing, amount=bid_amount)
                bid.save()
                return redirect(reverse("listing", args=[id]))
            else:
                return redirect(reverse("listing", args=[id]))
    else:
        return redirect(reverse("listing", args=[id]))




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
    bids = Bid.objects.filter(auction=listing).order_by('-amount')
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        if request.user not in listing.watchlist.all():
            listing.watchlist.add(request.user)
        else:
            listing.watchlist.remove(request.user)
        return redirect(reverse("listing", args=[id]))
    else:
        watchlist = request.user in listing.watchlist.all()
        if bids:
            highestbid = bids[0]
        else:
            highestbid = None

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": watchlist,
            "bid_form": BidForm,
            "bids": highestbid
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
