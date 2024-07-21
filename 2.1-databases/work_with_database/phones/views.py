from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort')
    if sort == 'name':
        phone_list = Phone.objects.all().order_by(sort)
    elif sort == 'max_price':
        phone_list = Phone.objects.all().order_by('price').reverse()
    elif sort == 'min_price':
        phone_list = Phone.objects.all().order_by('price')
    else:
        phone_list = Phone.objects.all()
    template = 'catalog.html'
    context = {'phones': phone_list}
    return render(request, template, context)


def show_product(request, slug):
    phone = Phone.objects.filter(slug=slug)[0]
    template = 'product.html'
    context = {'phone': phone}
    return render(request, template, context)
