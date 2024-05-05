from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
        return render(request, 'detalhes_filme.html', {'filme': filme, 'detalhes_filme': detalhes_filme, 'favorito':favorito})
    else:
        filme = get_object_or_404(Filme, id=filme_id)
        detalhes_filme = filme.detalhes()
        return render(request, 'detalhes_filme.html', {'filme': filme, 'detalhes_filme': detalhes_filme})
    

def detalhes_alimento(request, alimento_id):
    if request.user.is_authenticated:
        alimento = get_object_or_404(Alimento, id=alimento_id)
        usuario = request.user
        favorito = Favorito.objects.filter(usuario=usuario, alimento=alimento).exists()
        detalhes_alimento = alimento.detalhes()
        return render(request, 'detalhes_alimento.html', {'alimento': alimento, 'detalhes_alimento': detalhes_alimento, 'favorito':favorito})
    else:
        alimento = get_object_or_404(Alimento, id=alimento_id)
        detalhes_alimento = alimento.detalhes()
        return render(request, 'detalhes.html', {'alimento': alimento, 'detalhes_alimento': detalhes_alimento})

@login_required
def favoritar_filme(request, filme_id):
    filme = get_object_or_404(Filme, id=filme_id)
    
    if request.method == 'POST' or request.method == 'GET':
        usuario = request.user
        
        favorito_existente = Favorito.objects.filter(usuario=usuario, filme=filme).exists()
        
        if not favorito_existente:
            Favorito.objects.create(usuario=usuario, filme=filme)
        else:
            favorito = Favorito.objects.filter(usuario=usuario, filme=filme).first()
            favorito.delete()       
        return redirect('favoritos')
    
    return redirect('home')

@login_required
def favoritar_alimento(request, alimento_id):
    alimento = get_object_or_404(Filme, id=alimento_id)
    
    if request.method == 'POST' or request.method == 'GET':
        usuario = request.user
        
        favorito_existente = Favorito.objects.filter(usuario=usuario, alimento=alimento).exists()
        
        if not favorito_existente:
            Favorito.objects.create(usuario=usuario, alimento=alimento)
        else:
            favorito = Favorito.objects.filter(usuario=usuario, alimento=alimento).first()
            favorito.delete()       
        return redirect('favoritos')
    
    return redirect('home')

@login_required
def lista_favoritos(request):
    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(usuario=request.user)
        return render(request, 'favoritos.html', {'favoritos': favoritos})
    else:
        return redirect('login')

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