from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from .models import *

def home(request):
    filmes = Filme.objects.all()
    alimentos = Alimento.objects.all()
    return render(request, 'home.html', {'filmes': filmes}, {'alimentos': alimentos})

def detalhes_filme(request, filme_id):
    if request.user.is_authenticated:
        filme = get_object_or_404(Filme, id=filme_id)
        usuario = request.user
        favorito = Favorito.objects.filter(usuario=usuario, filme=filme).exists()
        detalhes_filme = filme.detalhes()
        return render(request, 'detalhes.html', {'filme': filme, 'detalhes_filme': detalhes_filme, 'favorito':favorito})
    else:
        filme = get_object_or_404(Filme, id=filme_id)
        detalhes_filme = filme.detalhes()
        return render(request, 'detalhes.html', {'filme': filme, 'detalhes_filme': detalhes_filme})

def getUser(req):
    user = User.objects.get(username=req.user)
    context = {"user": {"username": user.username,"email": user.email}}
    return context

        
class Search(View):
    def get(self, req):
        if(req.user.is_authenticated):
            context = getUser(req)
            
            searchTerm = req.GET.get("search")

            filmes = Filme.objects.all().filter(name__icontains=searchTerm)

            context["filmes"] = filmes

            return render(req, 'cinema_app/search.html', context)
        
        return render(req, 'cinema_app/signin.html')

class ReviewView(View):
    def get(self, req, id):
        if(req.user.is_authenticated):
            context = getUser(req)

            try:
                review = Review.objects.get(pk=id)
                filme = review.filme
                print(filme)

                context["filme"] = filme
                context["review"] = review

                return render(req, "cinema_app/review.html", context)
            except:
                return redirect("app:root")
            
        return redirect("app:root")
