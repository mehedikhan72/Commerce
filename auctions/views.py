from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid


def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all()
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

@login_required
def create_list(request, listed_by):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image_url = request.POST.get("image_url")
        category = request.POST.get("category")

        existing_titles = Listing.objects.values('name')
        t = []

        for n in existing_titles.iterator():
            t.append(n["name"])

        if name in t:
            return render(request, "auctions/error.html",{
                "message" : "Title already exists. Choose another one."
            })

        if not name:
            return render(request, "auctions/error.html",{
                "message" : "must enter a title!"
            })

        if not description:
            return render(request, "auctions/error.html",{
                "message" : "must enter a description!"
            })

        if not price:
            return render(request, "auctions/error.html",{
                "message" : "must enter a starting bid!"
            })

        if not image_url:
            return render(request, "auctions/error.html",{
                "message" : "must enter an image url!"
            })

        if not category:
            return render(request, "auctions/error.html",{
                "message" : "must enter a category!"
            })
        

        list_item = Listing.objects.create(name=name, description=description, price=price, image_url=image_url, category=category, listed_by=listed_by)
        list_item.save()

        # while creating an item, im also creating a bid instance for that item cause the starting bid would be the current bid.
        new_bid = Bid.objects.create(bid_item=name, starting_bid=price, current_bid=price, current_bidder=None, first_bid_made=True, bid_closed=False)
        new_bid.save()
        return HttpResponseRedirect(reverse("index"))

    categories = ["Fashion", "Toys", "Electronics", "Home", "Fantasy", "miscellaneous"]
    return render(request, "auctions/create_listing.html",{
        "categories" : categories
    })

def details(request, item):
    list_item = Listing.objects.filter(name=item).values().get()
    id = list_item["id"]
    name = list_item["name"]
    description = list_item["description"]
    price = list_item["price"]
    image_url = list_item["image_url"]
    category = list_item["category"]
    listed_by = list_item["listed_by"]
    created = list_item["created"]

    if request.user.is_authenticated:
        current_user = request.user.username
        watchlist_items = User.objects.get(username=current_user).watchlist.all()
        existing_watchlist = []
        for i in watchlist_items:
            existing_watchlist.append(i)

        already_exists = False
        for i in existing_watchlist:
            i = str(i)
            if i == name:
                already_exists = True
    else:
        watchlist_items = None
        existing_watchlist = None
        already_exists=None
    comments = Comment.objects.filter(comm_item=id).values()
    bid_data = Bid.objects.filter(bid_item=item).values().get()

    return render(request, "auctions/details.html",{
        "id" : id,
        "name" : name,
        "description" : description,
        "price" : price,
        "image_url" : image_url,
        "category" : category,
        "listed_by" : listed_by,
        "created" : created,
        "watchlist_items" : watchlist_items,
        "already_exists" : already_exists,
        "comments" : comments,
        "bid_data" : bid_data
    })

@login_required
def addtowatchlist(request, id, current_user):
    User.objects.get(username=current_user).watchlist.add(id)
    return HttpResponseRedirect(reverse("watchlist", args=(current_user,)))

@login_required
def removefromwatchlist(request, id, current_user):
    User.objects.get(username=current_user).watchlist.remove(id)
    return HttpResponseRedirect(reverse("watchlist", args=(current_user,)))

@login_required
def watchlist(request, current_user):
    watchlist_items = User.objects.get(username=current_user).watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "current_user" : current_user,
        "watchlist_items" : watchlist_items
    })
@login_required
def addcomments(request, item):
    if request.user.is_authenticated:
        current_user = request.user.username
    if request.method == "POST":
        comment = request.POST.get("comment")
        if not comment:
            return render(request, "auctions/error.html",{
                "message" : "Must enter a comment!"
            })

        item_id = Listing.objects.filter(name=item)[0]
        per_id = User.objects.filter(username=current_user)[0]

        c = Comment.objects.create(comm=comment, comm_item=item_id, comm_person=per_id)
        c.save()

        return HttpResponseRedirect(reverse("details", args=(item,)))

def categories(request):
    categories = ["Fashion", "Toys", "Electronics", "Home", "Fantasy", "miscellaneous"]
    return render(request, "auctions/categories.html",{
        "categories" : categories
    })

def category_items(request, category):

    listings = Listing.objects.filter(category=category).values()
    return render(request, "auctions/category_items.html",{
        "listings" : listings,
        "category" : category
    })

@login_required
def bidding(request, item):
    if request.user.is_authenticated:
        current_user = request.user.username

    if request.method == "POST":
        new_bid = request.POST.get("bid")

        if not new_bid:
            return render(request, "auctions/error.html",{
                "message" : "Must enter an amount!"
            })

        b = Bid.objects.get(bid_item=item)
        b.current_bid = new_bid
        b.current_bidder = current_user
        b.save()

    return HttpResponseRedirect(reverse("details", args=(item,)))

@login_required
def close_bidding(request, item):
    b = Bid.objects.get(bid_item=item)
    b.bid_closed = True
    b.save()

    l = Listing.objects.get(name=item)
    l.bid_closed = True
    l.save()
    

    return HttpResponseRedirect(reverse("details", args=(item,)))



