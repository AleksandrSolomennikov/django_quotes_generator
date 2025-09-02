from django.shortcuts import render, get_object_or_404, redirect
from .models import Quote, Source
from .forms import QuoteForm, SourceForm
import random
from django.views.decorators.http import require_POST
from django.db import transaction, models
from django.http import JsonResponse



def pick_weighted_random(quotes):
# quotes: list of Quote instances
    weights = [q.weight for q in quotes]
    chosen = random.choices(quotes, weights=weights, k=1)[0]
    return chosen

def index(request):
    qs = list(Quote.objects.all())
    if not qs:
        return render(request, 'quotes/index.html', {'quote': None})
    quote = pick_weighted_random(qs)
    # Increment views atomically
    with transaction.atomic():
        Quote.objects.filter(pk=quote.pk).update(views=models.F('views') + 1)
        # Refresh instance for display
        quote = Quote.objects.get(pk=quote.pk)
    return render(request, 'quotes/index.html', {'quote': quote})

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:index')
        return render(request, 'quotes/add_quote.html', {'form': form, 'sources_exist': Source.objects.exists()})
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form, 'sources_exist': Source.objects.exists()})


@require_POST
def vote_quote(request, pk):
    q = get_object_or_404(Quote, pk=pk)
    action = request.POST.get('action')
    if action == 'like':
        Quote.objects.filter(pk=q.pk).update(likes=models.F('likes') + 1)
    elif action == 'dislike':
        Quote.objects.filter(pk=q.pk).update(dislikes=models.F('dislikes') + 1)
    # If AJAX, return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        q.refresh_from_db()
        return JsonResponse({'likes': q.likes, 'dislikes': q.dislikes})
    return redirect('quotes:index')


def top10(request):
    top = Quote.objects.order_by('-likes', '-views')[:10]
    return render(request, 'quotes/top10.html', {'top': top})


def dashboard(request):
    # Simple dashboard: counts and latest
    total = Quote.objects.count()
    total_sources = sum(1 for _ in set(q.source_id for q in Quote.objects.all()))
    latest = Quote.objects.order_by('-created_at')[:10]
    return render(request, 'quotes/dashboard.html', {'total': total, 'total_sources': total_sources, 'latest': latest})

def add_source(request):
    # Простая форма создания источника, чтобы выпадающий список не был пустым
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:add_quote')
    else:
        form = SourceForm()
    return render(request, 'quotes/add_source.html', {'form': form})