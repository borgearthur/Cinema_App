from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

def home(request):
    context = {'home': True}
    return render(request, 'app/index.html', context)

class SignupView(View):
    def get(self, req):
        
        return render(req, 'app/signup.html')

    def post(self, req):
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        c_password = req.POST.get('c-password')

        user = User.objects.filter(username=username)

        if(user.exists()):
            messages.add_message(req, constants.ERROR, 'Username já existe!')
        else:
            if(password == ""):
                messages.add_message(req, constants.ERROR, 'Insira uma senha válida')
                return render(req, 'app/signup.html')
            
            if(password != c_password):
                messages.add_message(req, constants.ERROR, 'As senhas não são iguais!')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                return redirect('/')

        return render(req, 'app/signup.html')

def filmes(req):
    if(req.user.is_authenticated):
        return redirect('/app')
    
    return render(req, 'app/filmes.html')

def getUser(req):
    user = User.objects.get(username=req.user)
    context = {"user": {"username": user.username,"email": user.email}}
    return context


class ViewFilme(View):
    def get(self, req, id):
        if req.user.is_authenticated:
            context = getUser(req)
            try:
                filme = Filme.objects.get(pk=id)
                review = filme.review_set.filter(user=req.user)

                allReviews = filme.review_set.all().exclude(user=req.user)

                context["allReviews"] = allReviews

                if(review.exists()):
                    context["review"] = review.first()

                
                context["filme"] = filme
                
               
                try:
                    user_review = Review.objects.get(user=req.user, filme=filme)
                    context["user_review"] = user_review.text
                except Review.DoesNotExist:
                    context["user_review"] = None
                return render(req, 'app/filme.html', context)
            except Exception as e:
                print("An error occurred:", e)
                return redirect("app:root")
        
        return redirect("autenticacao:signin")

    def post(self, req, id):
        if req.POST.get("action") == "submit_review":
            return self.criandoReview(req, id)
        else:
            return self.like_game(req, id)

    def criandoReview(self, req, id):
        if req.user.is_authenticated:
            try:
                filme = Filme.objects.get(pk=id)
                review_text = req.POST.get('textoDaReview')

                existing_review = Review.objects.filter(user=req.user, filme=filme).first()

                if existing_review:
                    existing_review.text = review_text
                    existing_review.save()
                    return redirect(f"/app/review/{existing_review.id}")
                
                else:
                    novaReview = Review(user=req.user, filme=filme, text=review_text)
                    novaReview.save()

                    return redirect(f"/app/review/{novaReview.id}")
            except Filme.DoesNotExist:
                return HttpResponse({"message": "Filme não encontrado"}, status=404)
            
        else:
            return HttpResponse({"message": "Você precisa estar logado"}, status=400)

class ReviewView(View):
    def get(self, req, id):
        if(req.user.is_authenticated):
            context = getUser(req)

            try:
                review = Review.objects.get(pk=id)
                game = review.game
                print(game)

                context["game"] = game
                context["review"] = review

                return render(req, "app/review.html", context)
            except:
                return redirect("app:root")
            
        return redirect("app:root")

@login_required
def criar_filme(request):
    if request.method == 'POST':
        form = FormFilme(request.POST, user=request.user)
        if form.is_valid():
            filme = form.save(commit=False)
            filme.user = request.user
            filme.save()
            return redirect('products')
    else:
        form = FormFilme(user=request.user)
    return render(request, 'app/product_form.html', {'form': form})

@login_required
def create_category(request):
    error_message = ''
    if request.method == 'POST':
        form = FormGenero(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('product-create')
    else:
        form = FormGenero()
    return render(request, 'app/create_category.html', {'form':form})