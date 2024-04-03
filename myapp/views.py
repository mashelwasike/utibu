from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request,'store/index.html')

def collection(request):
    category = Category.objects.filter(status = 0)
    context={'category':category}
    return render(request, 'store/collection.html',context)

def collectionview(request,slug):
    if(Category.objects.filter(slug =slug,status = 0)):
        products = Medicine.objects.filter(category__slug = slug)
        category= Category.objects.filter(slug=slug).first()
        context ={'products':products,'category':category}
        return render(request, 'store/products/products.html',context)
    
    else:
        messages.warning(request,'no such category')
        return redirect('collection')
    
def productview(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug = cate_slug,status=0)):
        if(Medicine.objects.filter(slug= prod_slug,status=0)):
            products = Medicine.objects.filter(slug= prod_slug,status=0).first()
            context ={'products':products}
        else:
            messages.info(request,"no such product")
            return redirect('collection')
    else:
        messages.error(request,"No such category")
        return redirect('collection')
    return render(request,'store/products/view.html',context)

def productlist(request):
    products = Medicine.objects.filter(status = 0).values_list('name',flat=True)
    mylist = list(products)
    return JsonResponse(mylist,safe=False)

def searchproduct(request):
    if request.method == "POST":
        searchItem = request.POST.get('productsearch')
        if searchItem == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Medicine.objects.filter(name__contains=searchItem).first()

            if product:
                return redirect('collection/'+product.category.slug+'/'+ product.slug)
            else:
                messages.info(request,"product not found")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

    
