from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import ProductModel,OrderModel,DetailModel
from smtplib import SMTP
from email.mime.text import MIMEText

# Create your views here.
cartlist=[]
shipping=100 #運費
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
    global cartlist
    #add
    if type=='add':
        product=ProductModel.objects.get(id=id)
        #購物車有沒有存在的商品?
        #如果有舊更新session裡面的商品數量、金額
        #沒有就把商品放到session
        noCartSession=True
        for unit in cartlist:
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
            cartlist.append(templist)
        request.session['cartlist']=cartlist
        print(request.session['cartlist'])
        return redirect('/cart/')
    #empty
    elif type=='empty':
        cartlist=[]
        request.session['cartlist']=cartlist
        return redirect('/cart/')
    #update
    elif type=='update':
        if request.method=='POST':
            n=1
            for unit in cartlist:
                unit[2]=request.POST.get('quantity'+str(n),'1')
                unit[3]=str(int(unit[1])*int(unit[2]))
                n=n+1
                request.session['cartlist']=cartlist
            return redirect('/cart/')
    #remove
    elif type=='remove':
        del cartlist[int(id)] #這個ID是cartlist的索引值
        request.session['cartlist']=cartlist
        return redirect('/cart/')

def cart(request):
    global cartlist
    global shipping
    #locals是將裡面的區域變數傳到網頁，所以要將全域轉區域
    localcartlist=cartlist
    localshipping=shipping
    total=0 #小計
    for unit in localcartlist:
        total=total+int(unit[3])
    grandtotal=total+localshipping #總價(加上運費價格)
    return render(request,'cart.html',locals())

def cartorder(request):
    global cartlist
    global shipping
    localcartlist=cartlist
    localshipping=shipping
    total=0 #小計
    for unit in localcartlist:
        total=total+int(unit[3])
    grandtotal=total+localshipping
    return render(request,'cartorder.html',locals())
def cartok(request):
    global cartlist
    global shipping
    if request.method=='POST':
        customername=request.POST['customername']
        customerphone=request.POST['customerphone']
        customeremail=request.POST['customeremail']
        customeraddress=request.POST['customeraddress']
        paytype=request.POST['paytype']
        #print(customername+customerphone+customeremail+customeraddress+paytype)
        total=0 #小計
        for unit in cartlist:
            total=total+int(unit[3])
        grandtotal=total+shipping #總價(加上運費價格)

        #---將訂購資訊寫進OrderModel表單---
        productOrder=OrderModel.objects.create(customername=customername,
        customerphone=customerphone,customeremail=customeremail,customeraddress
        =customeraddress,paytype=paytype,grandtotal=grandtotal,shipping=shipping,
        subtotal=total)
        productOrder.save()
        #---將該筆訂單，寫進DetailModel表單---
        #---訂單不會只有一筆，用for一筆一筆放入---
        dtotal=0
        for unit in cartlist:
            dtotal=int(unit[1])*int(unit[2])
            unitDetail=DetailModel.objects.create(pname=unit[0],unitprice=int(unit[1]),quantity=int(unit[2]),dtotal=dtotal,dorder=productOrder)
            unitDetail.save()
        cartlist=[]
        #---郵件寄送------
    mailfrom='a2166899@gmail.com'
    mailpw='evjpwyszphbuugng'
    mailto=customeremail
    mailsubject='Tommy 商店通知'
    mailcontent='親愛的'+customername+'，你的訂單已完成，目前正在火速處理，請耐心等候'
    send_message(mailfrom,mailpw,mailto,mailsubject,mailcontent)
    return render(request,'cartok.html',locals())

def send_message(mailfrom,mailpw,mailto,mailsubject,mailcontent):
    strSmtp='smtp.gmail.com:587'
    strAccount=mailfrom
    strPassword=mailpw
    msg=MIMEText(mailcontent)
    msg['Subject']=mailsubject
    mailto1=mailto
    server=SMTP(strSmtp)
    server.ehlo() #跟主機溝通
    server.starttls() #TTLS安全認證
    server.login(strAccount,strPassword)
    server.sendmail(strAccount,mailto1,msg.as_string())
