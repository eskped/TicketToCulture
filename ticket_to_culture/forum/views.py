from sre_constants import SUCCESS
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from .models import Profile, Post, Rating
from .forms import SignUpForm, UpdateUserForm, UpdateProfileForm, CreatePostForm, FilterPosts
from ticket_to_culture.settings import MEDIA_ROOT, MEDIA_URL


@login_required
def create_post(request):
    user = request.user
    if request.method == "GET":
        form = CreatePostForm()
        return render(request, 'post/createPost.html', {'form': form})
    elif request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid() and user.is_authenticated:
            form = form.cleaned_data
            post = Post(user=user, title=form["title"], description=form["description"], is_sale=form["is_sale"],
                        price=form["price"], image=form["image"], location=form["location"], type=form["type"])
            post.save()
            return HttpResponseRedirect(reverse('forum:myPosts'))
        return HttpResponse("ikke valid")
    


@login_required
def profile_page(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            form = profile_form.save()
            form.image = profile_form.cleaned_data.get('image')
            user_form.save()
            profile_form.save()

    else:
        template = loader.get_template('user/profile.html')
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        # Calculate average score
        my_ratings = Rating.objects.filter(rated_user=request.user)
        totalScore = 0
        for r in my_ratings:
            totalScore += r.rating_value
        if len(my_ratings) == 0:
            score = "Ikke vurdert"
        else:
            score = str(round(totalScore / len(my_ratings), 2)) + "/5.0"

        # Get user info
        user = request.user
        context = {
            "image": user.profile.image,
            "username": user.username,
            "email": user.email,
            'user_form': user_form,
            'profile_form': profile_form,
            'phone': user.profile.phone,
            'score': score,
        }
        return HttpResponse(template.render(context, request))

    # Get user info
    user = request.user
    context = {
        "image": user.profile.image,
        "username": user.username,
        "email": user.email,
        'user_form': user_form,
        'profile_form': profile_form,
        'phone': user.profile.phone
    }
    return render(request, 'user/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('/profile')

    else:
        password_form = PasswordChangeForm(request.user)
        template = loader.get_template('user/change-password.html')
    return render(request, 'user/change-password.html', {'password_form': password_form})

# View for when seller gives rating to a buyer.
@login_required
def rate_buyer(request, sold_id, buyer_id):
    if request.method == "GET":
        return render(request, "rating/rate-buyer.html", {"sold_id": sold_id, "buyer_id": buyer_id}, )
    else:
        # Seller gives a rating to buyer:
        rate_text = request.POST["rating"]
        rating = 0
        try:
            rating = int(rate_text)
        except:
            raise SuspiciousOperation(
                "Rating value cannot be casted to an int")
        post = Post.objects.get(pk=sold_id)
        buyer = User.objects.get(pk=buyer_id)
        Rating.objects.create(rated_user=buyer, rated_by_user=post.user,
                              rating_value=rating, is_seller_rating_buyer=True, post=post)
        return redirect("forum:sellPost", sold_id)


# View for when buyer gives rating to a seller.
# @seller_rating_id is the ID for the rating the seller gave to buyer.
@login_required
def rate_seller(request, seller_rating_id):
    if request.method == "GET":
        return render(request, "rating/rate-seller.html", {"seller_rating_id": seller_rating_id}, )
    else:
        # Buyer gives a rating to buyer:
        rate_text = request.POST["rating"]
        rating = 0
        try:
            rating = int(rate_text)
        except:
            raise SuspiciousOperation(
                "Rating value cannot be casted to an int")
        # Create buyer rating in reponse to seller rating:
        seller_rating = Rating.objects.get(pk=seller_rating_id)
        seller_user = seller_rating.rated_by_user
        post = seller_rating.post
        Rating.objects.create(rated_user=seller_user, rated_by_user=request.user, rating_value=rating,
                              post=post, rated_user_responded=True, is_seller_rating_buyer=False)
        # Set responded to True on seller rating of buyer:
        seller_rating.rated_user_responded = True
        seller_rating.save()
        return redirect("forum:myPosts")


# View for searching for the buyers username, to give a rating.
@login_required
def rate_buyer_search(request, sold_id):
    print("sold_id:: " + str(sold_id))
    if request.method == "GET":
        return render(request, "rating/search.html", {"sold_id": sold_id})
    elif request.method == "POST":
        formdata = request.POST
        users = User.objects.filter(username__contains=formdata["search"])
        return render(request, "rating/search.html", {"results": users, "sold_id": sold_id})


@login_required
def my_posts(request):
    if request.method == "GET":
        template = loader.get_template('user/my-posts.html')
        # Get posts info
        user = request.user
        active_posts = Post.objects.filter(user=user).filter(is_sold=False)
        old_posts = Post.objects.filter(user=user).filter(is_sold=True)
        ratings_available = Rating.objects.filter(rated_user=user).filter(
            rated_user_responded=False).filter(is_seller_rating_buyer=True)
        context = {
            "active_posts": active_posts,
            "old_posts": old_posts,
            "ratings_available": ratings_available,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("unknown")


@login_required
def sell_post(request, sold_id):
    post = get_object_or_404(Post, pk=sold_id)
    post.is_sold = True
    post.save()
    return redirect('forum:myPosts')


@login_required
def undo_sold(request, sold_id):
    post = get_object_or_404(Post, pk=sold_id)
    post.is_sold = False
    post.save()
    return redirect('forum:myPosts')


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                HttpResponse(f"You are now logged in as {username}.")
                return redirect("/")
            else:
                HttpResponse("Invalid username or password.")
        else:
            HttpResponse("Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'auth/signin.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile.html instance created by the signal
            user.profile.phone = form.cleaned_data.get('phone_number')
            user.profile.image = form.cleaned_data.get('image')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


def discovery_page(request):
    signedin = request.user.is_authenticated
    template = loader.get_template('discovery/discovery_page.html')
    post_list = Post.objects.filter(is_sold=False)
    form = FilterPosts(request.POST)
    
    if(request.method == "POST"):
        form = FilterPosts(request.POST)
        # Sorterer på pris, lav-til-høy
        if form["priceLowHigh"].value() == True:
            post_list = post_list.filter(is_sold=False).order_by('price')

        # Sorterer på om annonsen er til salgs 
        if form["for_sale"].value() == True:
            post_list = post_list.filter(is_sale=True)

        # Sorterer på om annosen ønskes kjøpt
        if form["for_buy"].value() == True:
            post_list = post_list.filter(is_sale=False)

        # Filterer på lokasjon
        if(form['location'].value() != "lokasjon"):
            by = form['location'].value()
            post_list = post_list.filter(location=by)

        # Filterer på type arrangement  
        if(form['type'].value() != "arrangement"):
            arrangement = form['type'].value()
            post_list = post_list.filter(type=arrangement)
        
        submitbutton = request.POST.get('Submit')
        #post_list = post_list.filter(is_sold=False)
        context = {
                'post_list': post_list,
                'form': form,
                'submitbutton': submitbutton,
            }
        return HttpResponse(template.render(context, request))
        
        
    if(request.method == "GET"):

        if signedin:
            context = {
                'post_list': post_list,
                'form': form,
            }
            return HttpResponse(template.render(context, request))
        else:
            context = {
            'post_list': post_list,
            'form': form,
            }
        return HttpResponse(template.render(context, request))
    else:
        context = {
            'post_list': post_list,
        }

    return HttpResponse(template.render(context, request))

@login_required
def post(request, post_id):
    post = Post.objects.get(pk = post_id)

    # Calculate average score
    seller_ratings = Rating.objects.filter(rated_user=post.user)
    totalScore = 0
    for r in seller_ratings:
        totalScore += r.rating_value
    if len(seller_ratings) == 0:
        score = "Ikke vurdert"
    else:
        score = str(round(totalScore / len(seller_ratings), 2)) + "/5.0"

    context = {
        'post': post,
        'seller_rating': score,
    }
    template = loader.get_template('post/post.html')
    return HttpResponse(template.render(context, request))




