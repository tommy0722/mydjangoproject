from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import ProductModel
# Create your views here.
carlist=[]
def index(request):
    products=ProductModel.objects.all()
    productlist=[]
    for i in range(1,9):
        product=ProductModel.objects.get(id=i)
        productlist.append(product)
    return render(request,'index.html',locals())

def detail(request,id=None):
    product=ProductModel.objects.get(id=id)
    return render(request,'detail.html',locals())

def addtocart(request,type=None,id=None):
    global carlist
    #add
    if type=='add':
        product=ProductModel.objects.get(id=id)
        #購物車有沒有存在的商品?
        #如果有舊更新session裡面的商品數量、金額
        #沒有就把商品放到session
        noCartSession=True
        for unit in carlist:
            if product.pname ==unit[0]:
                unit[2]=str(int(unit[2])+1)
                unit[3]=str(int(unit[3])+product.pprice*1)
                noCartSession=False
        if noCartSession:
            templist=[]
            templist.append(product.pname)
            templist.append(str(product.pprice))
            templist.append(str(1))
            templist.append(str(product.pprice*1))
            carlist.append(templist)
        request.session['cartlist']=carlist
        print(request.session['cartlist'])
        return redirect('/cart/')
    #update
    #empty
    #remove
def cart(request):
    return HttpResponse('這裡是購物車')