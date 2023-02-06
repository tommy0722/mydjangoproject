from django.contrib import admin

# Register your models here.
from .models import ProductModel,OrderModel,DetailModel
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('pname', 'pprice', 'pimage','pdescription')
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id','subtotal', 'shipping', 'grandtotal','customername'
    ,'customerphone','customeremail','customeraddress','paytype')
    search_fields = ('customername',)
class DetailModelAdmin(admin.ModelAdmin):
    list_display = ('id','dorder', 'pname', 'unitprice','quantity','dtotal')
admin.site.register(ProductModel,ProductModelAdmin)
admin.site.register(OrderModel,OrderModelAdmin)
admin.site.register(DetailModel,DetailModelAdmin)
