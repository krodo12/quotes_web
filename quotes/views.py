import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quote
from .forms import QuoteForm
from django.db.models import Sum


def random_quote(request, n=10):
    # если в сессии уже есть сохранённые цитаты – показываем их
    if 'current_quotes' in request.session:
        ids = request.session['current_quotes']
        quotes = list(Quote.objects.filter(id__in=ids))
    else:
        # генерим новые
        quotes = list(Quote.objects.all())
        if not quotes:
            return render(request, "quotes/random_quote.html", {"quotes": []})

        weights = [q.weight for q in quotes]
        selected_quotes = random.sample(quotes, min(n, len(quotes)))  # без повторов
        quotes = selected_quotes

        # сохраним их в сессию
        request.session['current_quotes'] = [q.id for q in quotes]

        # увеличим просмотры только один раз
        viewed = request.session.get('views', [])
        for quote in quotes:
            if str(quote.id) not in viewed:
                quote.views += 1
                quote.save()
                viewed.append(str(quote.id))
        request.session['views'] = viewed
        request.session.modified = True

    return render(request, "quotes/random_quote.html", {"quotes": quotes})


def refresh_quotes(request, n=10):
    """Принудительно обновить подборку цитат"""
    if 'current_quotes' in request.session:
        del request.session['current_quotes']
    return redirect('random_quote')

def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("random_quote")  
    else:
        form = QuoteForm()

    return render(request, "quotes/add_quote.html", {"form": form})

def quote_detail(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)

    viewed = request.session.get('views', set())
    # Сессия хранит строки, так что используем str(quote.id)
    if str(quote.id) not in viewed:
        quote.views += 1
        quote.save()
        viewed.add(str(quote.id))
        request.session['views'] = viewed
        request.session.modified = True

    return render(request, 'quotes/random_quote.html', {'quote': quote})


def toggle_like(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    likes = request.session.get('likes', {})

    if str(quote.id) in likes:
        quote.likes = max(quote.likes - 1, 0)
        likes.pop(str(quote.id))
    else:
        quote.likes += 1
        likes[str(quote.id)] = True

    quote.save()
    request.session['likes'] = likes
    request.session.modified = True
    return redirect('random_quote')


def toggle_dislike(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    dislikes = request.session.get('dislikes', {})

    if str(quote.id) in dislikes:
        quote.dislikes = max(quote.dislikes - 1, 0)
        dislikes.pop(str(quote.id))
    else:
        quote.dislikes += 1
        dislikes[str(quote.id)] = True

    quote.save()
    request.session['dislikes'] = dislikes
    request.session.modified = True
    return redirect('random_quote')


def top_quotes(request):
    quotes = Quote.objects.order_by("-likes")[:10]
    return render(request, "quotes/top_quotes.html", {"quotes": quotes})

def dashboard(request):
    total_quotes = Quote.objects.count()
    total_likes = Quote.objects.aggregate(Sum('likes'))['likes__sum'] or 0
    total_dislikes = Quote.objects.aggregate(Sum('dislikes'))['dislikes__sum'] or 0
    total_views = Quote.objects.aggregate(Sum('views'))['views__sum'] or 0

    top_quotes = Quote.objects.order_by('-likes')[:5]
    latest_quotes = Quote.objects.order_by('-id')[:5]

    context = {
        'total_quotes': total_quotes,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_views': total_views,
        'top_quotes': top_quotes,
        'latest_quotes': latest_quotes,
    }
    return render(request, 'quotes/dashboard.html', context)