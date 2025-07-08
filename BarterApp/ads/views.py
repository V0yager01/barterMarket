from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .const import DELETE_CONFIRM_MESSAGE, DELETE_SUCCESS
from .forms import AdForm, ExchangeProposalForm
from .models import Ad, ExchangeProposal, Category

from .const import CONDITION_CHOICES


def main_page(request):
    ads = Ad.objects.all()
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')
    page_number = request.GET.get('page')

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads.order_by('-created_at'), 10)
    page_obj = paginator.get_page(page_number)
    category_list = Category.objects.all()

    context = {
        'ads': page_obj,
        'query': query,
        'category': category,
        'condition': condition,
        'condition_choices': CONDITION_CHOICES,
        'paginator': paginator,
        'page_obj': page_obj,
        'category_list': category_list
    }
    return render(request, 'ads/ad_light.html', context)


@login_required()
def create_ad(request: HttpRequest):
    form = AdForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('main:index')
    return render(request,
                  'ads/adform.html',
                  {'form': form})


@login_required()
def ad_page(request: HttpRequest, id: int):
    ad = get_object_or_404(Ad, id=id)
    context = {'ad': ad}
    return render(request,
                  template_name='ads/ad_page.html',
                  context=context)


@login_required()
def rm_ad(request: HttpRequest, id: int):
    ad = get_object_or_404(Ad, user=request.user, id=id)
    if request.method == 'POST':
        ad.delete()
        context = {
            'title': DELETE_SUCCESS
            }
        return render(request=request,
                      template_name='ads/delete_success_page.html',
                      context=context)
    context = {
        'ad': ad,
        'title': DELETE_CONFIRM_MESSAGE
        }
    return render(request=request,
                  template_name='ads/delete_confirm_page.html',
                  context=context)


@login_required()
def update_ad(request: HttpRequest, id: int):
    ad = get_object_or_404(Ad, user=request.user, id=id)
    form = AdForm(request.POST or None, request.FILES or None, instance=ad)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('main:detail', id=ad.id)
    return render(request, 'ads/adform.html', {'form': form, 'ad': ad})


@login_required
def trade_page(request):
    trades = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user)
    )
    status = request.GET.get('status')
    direction = request.GET.get('direction')

    if status:
        trades = trades.filter(status=status)
    if direction == 'sent':
        trades = trades.filter(ad_sender__user=request.user)
    elif direction == 'received':
        trades = trades.filter(ad_receiver__user=request.user)

    context = {
        'trades': trades,
        'status_selected': status,
        'direction_selected': direction,
    }
    return render(request, 'trades/trade_page.html', context)


@login_required()
def create_trade(request: HttpRequest, id: int):
    ad_receiver = get_object_or_404(Ad, id=id)
    if ad_receiver.user == request.user:
        title = 'Нельзя обменивать у самого себя!!'
        context = {'title': title}
        return render(request, 'trades/trade_message.html', context=context)
    ad_sender = Ad.objects.filter(user=request.user).all()
    if not ad_sender.exists():
        title = 'У вас нет объявлений, чтобы предложить обмен'
        context = {'title': title}
        return render(request, 'trades/trade_message.html', context=context)

    form = ExchangeProposalForm(request.POST or None, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad_receiver
            proposal.save()
            return redirect('main:index')

    return render(request, 'trades/create_trade.html', {
        'form': form,
        'title': 'Создать предложение обмена',
        'ad_receiver': ad_receiver
    })


@require_POST
@login_required
def update_trade_status(request: HttpRequest, id: int):
    trade = get_object_or_404(ExchangeProposal, id=id)
    if trade.ad_receiver.user == request.user:
        action = request.POST.get('action')
        if action == 'accept':
            trade.status = 'accepted'
        elif action == 'reject':
            trade.status = 'rejected'
        trade.save()
    elif trade.ad_sender.user == request.user:
        if trade.status == 'pending' and request.POST.get('action') == 'cancel':
            trade.status = 'rejected'
            trade.save()
    return redirect('main:trade')
