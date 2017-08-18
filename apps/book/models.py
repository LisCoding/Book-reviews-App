from __future__ import unicode_literals
from django.db import models
import re
from myemail import Email
from name import Name
from password import Password
import traceback

class UserManager(models.Manager):
    # def validate(self,post_data):
    #     errors = {}
    #     pwd = User.objects.filter(email=request.POST["email"]).values("password")
    #     if len(pwd) == 0:
    #         return redirect("/login")
    #     # to check if the password are equal
    #     hash1 = pwd[0]["password"]
    #     pwd2=request.POST["pwd"]
    #     if bcrypt.checkpw(pwd2.encode(), hash1.encode()):
    def validate(self, post_data):
        errors = {}
        valid_first_name = "django"
        valid_last_name  = "django"
        try:
            Name(post_data["f_name"], valid_last_name)
        except Exception as e:
            errors["f_name"] = str(e)
        try:
            Name(valid_first_name, post_data["l_name"])
        except Exception as e:
            errors["l_name"] = str(e)

        try:
            Password(post_data["pwd"], post_data["confi_pwd"])
        except Exception as e:
            errors["pwd"] = str(e)
            traceback.print_exc()

        # check email field for valid email
        try:
            Email(post_data['email'])
        except Exception as e:
            errors['email'] = str(e)

        # if email is valid check db for existing email
        if "email" not in errors:
            if len(self.filter(email=post_data['email'])) >= 1:
                errors['email'] = "email already in use"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    # def __str__(self):
    #     return self.email
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    review = models.TextField(default="N/A")
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # user can have many reviews
    reviewer = models.ForeignKey(User, related_name = "reviewed_books")

    #book can have many reviews
    book = models.ForeignKey(Book, related_name = "uploaded_reviews")
