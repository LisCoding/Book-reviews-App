from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import error
import bcrypt
from models import *

def index(request):
    # context = {
    #     "user_info": User.objects.all().values()
    # }
    return render(request,'book/index.html')

def display_books(request):
    books = Book.objects.all()
    context = {
        "books" : books,
    }
    return render(request,'book/display.html', context)

def new(request):
    return render(request,'book/add.html')

def show(request,id):
    return render(request,'book/show.html')

def display_user(request,id):
    return render(request,'book/user.html')

def authentification(request):
    pwd = User.objects.filter(email=request.POST["email"]).values("password")
    if len(pwd) == 0:
        return redirect("/")
    # to check if the password are equal
    hash1 = pwd[0]["password"]
    pwd2=request.POST["pwd"]
    if bcrypt.checkpw(pwd2.encode(), hash1.encode()):
        request.session["user_id"] = User.objects.get(email=request.POST["email"]).id
        return redirect("/books")
    else:
        return redirect("/")

def create(request):
    errors = User.objects.validate(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    pwd_hash = bcrypt.hashpw(request.POST["pwd"].encode(), bcrypt.gensalt())
    User.objects.create(first_name=request.POST["f_name"], last_name=request.POST["l_name"], alias=request.POST["alias"], email= request.POST["email"], password= pwd_hash)
    request.session["user_id"] = User.objects.get(email=request.POST["email"]).id
    return redirect("/books")

def book_review(request, user_id):
    user = User.objects.get(id=user_id)
    book = Book.objects.filter(title=request.POST["title"])
    if len(book) == 0:
        b_reviewed = Book.objects.create(title=request.POST["title"], author=request.POST["name_author"])
        Review.objects.create(review=request.POST["review"], rating=request.POST["stars"],reviewer=user, book=b_reviewed)
    else:
        book_obj = Book.objects.get(author=request.POST["name_author"])
        Review.objects.create(review=request.POST["review"], rating=request.POST["stars"],reviewer=user, book=book_obj)
    return redirect("/books")
# def show(request, id):
#     if request.method == "GET":
#         context = {
#             "user" : User.objects.get(id=id)
#         }
#         return render(request,'user_app/show.html', context)
#     else:
#         # TODO: find a way to pass id into the url when we redirecting
#
#         return HttpResponse("hello!!")
#         # request.session["id"]= User.objects.get(id=id).id
#         #
#         # return redirect("/user/update")
#
# def update(request, id):
#     user = User.objects.get(id=id)
#     user.first_name = request.POST["f_name"]
#     user.last_name = request.POST["l_name"]
#     user.email = request.POST["email"]
#     user.save()
#     return redirect("/user")
#

#
# def edit(request, id):
#     context = {
#         "user" : User.objects.get(id=id)
#     }
#     return render(request,'user_app/edit.html', context)
#
# def create(request):
#     data = User.objects.create(first_name=request.POST["f_name"], last_name=request.POST["l_name"], email=request.POST["email"])
#     print data.first_name, data.last_name
#     return redirect("/user/new")
#
# def delete(request, id):
#     user = User.objects.get(id=id)
#     user.delete()
#
#     return redirect("/user")
