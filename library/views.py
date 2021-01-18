from django.shortcuts import render,redirect
from .models import Profile,Book,User
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from .forms import BookForm,UpdateUser
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib import auth
# Create your views here.
def index(request):
   return render(request,'library/Home.html',{
      "page":"Home"
   })

def show_books(request):
   books = Book.objects.all()
   return render(request,"library/show_books.html",{
      "books":books,
      "counter":0,
      "page":"Books"
   })

def user_Profile(request):
    if request.user.is_authenticated:
       
       books = request.user.profile.books.all()
       if books.count() == 0:
          books = None
      
       return render(request,"library/user_profile.html",{
          "user":User.objects.get(username=request.user.username),
          "show":"user_profile",
          "page":"profile"
       })

def profile_(request):
    
    return render(request,"library/user_profile.html",{
          "user":User.objects.get(username=request.user.username),
          "show":"user_profile",
          "page":"profile"
       })
def user_books_(request):
     user = User.objects.get(username=request.user.username)
     books = user.profile.books.all()
     return render(request,"library/user_profile.html",{
          "books":books,
          "show":"books",
          "book_count":books.count(),
          "page":"profile"
       })

def issue_books(request):
    user_books = request.user.profile.books.all()
    books = []
    if user_books.count()==0:
       books = Book.objects.all()
    else:
       avalaible = Book.objects.all()
       for book in avalaible:
          if book not in user_books:
             books.append(book)
       print(books)
    return render(request,"library/issue_books.html",{
       "books_avalaible" : books,
       "message":None,
       "page":"Issue books"
    })

def add(request,book_id):
    book = Book.objects.get(book_id = book_id)
    books=[]
    request.user.profile.books.add(book)
    request.user.save()
    book.avalaible = book.avalaible - 1
    user_books = request.user.profile.books.all()
    avalaible = Book.objects.all()
    for book in avalaible:
         if book not in user_books:
             books.append(book)
    return render(request,"library/issue_books.html",{
       "books_avalaible" : books,
       "message":"Book added successfully",
       "page":"add a book"
    })

  
def Add(request):
   if request.method == "POST":
       
       book_id = Book.objects.count()+1
       book_name = request.POST['book_name']
       book_author = request.POST['book_author']
       description = request.POST['description']
       avalaible = request.POST['avalaible']
       image = request.POST['book_image']
       category = request.POST['category']
       book = Book(book_id,book_name,book_author,description,avalaible,image,category)
       book.save()
       return redirect('add_book',)    
   else:
       return HttpResponse('error')



def return_book(request,book_id):
    b = Book.objects.get(book_id = book_id)
    request.user.profile.books.remove(b)
    return render(request,'library/user_profile.html',{
       "message":"book removed",
       "show":"books",
       "books":request.user.profile.books.all(),
       "page":"profile"
    })

def update(request):
    return render(request,'library/user_profile.html',{
       "show":"update_profile",
       "form":UpdateUser(),
       "page":"profile"
    })
def update_profile(request):
    if request.method == "POST":
       form = UpdateUser(request.POST)
       if form.is_valid():
            
            request.user.username = form.cleaned_data.get('username')
            request.user.first_name = form.cleaned_data.get('first_name')
            request.user.last_name = form.cleaned_data.get('last_name')
            request.user.email = form.cleaned_data.get('email')
            request.user.password1 = form.cleaned_data.get('password1')
            request.user.password2 = form.cleaned_data.get('password2')
            request.user.save()
            raw_password = form.cleaned_data.get('password1')
            user  = authenticate(username = request.user.username ,password=raw_password)
            auth.login(request,user)
            return render(request,'library/user_profile.html',{
               "show":"user_profile",
               "message":"updated profile",
               "page":"profile"
            })
       else:
           return render(request,'library/user_profile.html',{
             "show":"update_profile",
              "form":UpdateUser(),
              "message":"Incorrect details",
              "page":"profile"
          })
    else:
       return render(request,'library/user_profile.html',{
             "show":"update_profile",
              "form":UpdateUser(),
              "message":"Incorrect method",
              "page":"profile"
          })


categories = ['Algorithm','Programming','Artificial Intelligence']
def categoryshow(request,category_no):
    books = Book.objects.filter(category = categories[category_no - 1])
    return render(request,'library/show_books.html',{
      "books":books,
      "counter":0,
      "page":"Books"
    })
