from django.contrib import admin
from CRM.models import Profile, Chart, ChartItem, Shipping, Order, Sample, Sampler,Discount

class ShippingStackedAdmin(admin.StackedInline):
    model = Shipping

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    inlines = [ShippingStackedAdmin,]
    #list_display = ('user.email')

class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    list_display = ('percentage','code','number_use','actual_use','deadline')
    readonly_fields = ('actual_use',)

class ChartItemAdmin(admin.ModelAdmin):
    model = ChartItem
    list_display = ('id','chart','product','status','chart__user')

    def chart__user(self, obj):
        if obj.chart and obj.chart.user:
            return obj.chart.user
        else :
            return "User Non Reg"

class OrderAdmin(admin.ModelAdmin):
    model = Order

    list_display = ('internal_tracking_id','shipping_tracking_id','user_','created_at','modified_at','order_status','final_payment','is_sampler','_is_paid')

    def _is_paid(self, obj):
        return obj.is_paid()

    def user_(self, obj):
        da_user = obj.user()
        if da_user:
            return da_user         
        else :
            return 'No User'
        
    #inlines = ('inte',)

class ShippingAdmin(admin.ModelAdmin):
    list_display = ("user","email","fullname","country","city","CAP","shipping_address","telephone_num","is_active")
    model = Shipping

class ChartItemStackedAdmin(admin.StackedInline):
    model = ChartItem

    search_fields = ('product__code', )
    readonly_fields  = ('status','modified_at')

def close_them(modeladmin, request, queryset):
    for e in queryset:
        e.completion_status = 'cs'
        e.save() 

close_them.short_description = "Mark as Closed"


class ChartAdmin(admin.ModelAdmin):
    model = Chart

    list_display = ('session_id','user','completion_status','created_at','modified_at',
    '_num_prods','order', '_is_paid')
    actions = [close_them]
    readonly_fields  = ( 'session_id','created_at','modified_at')

    inlines = [ChartItemStackedAdmin]

    def _num_prods(self, obj):
        return obj.all_items()

    def _is_paid(self, obj):
        return obj.is_paid()

    _num_prods.short_description = "Number of Products"
    _num_prods.admin_order_field = 'num_prods'


class SampleStackedAdmin(admin.StackedInline):
    model = Sample

    search_fields = ('product__code', )
    readonly_fields  = ('status','modified_at')


class SamplerAdmin(admin.ModelAdmin):
    model = Sampler
    list_display = ( 'session_id','user','created_at','modified_at','_is_paid','order')
    readonly_fields  = ( 'session_id','created_at','modified_at','order')
    inlines = [SampleStackedAdmin]

    def _is_paid(self, obj):
        return obj.is_paid()

admin.site.register(Discount,DiscountAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Chart,ChartAdmin)
admin.site.register(ChartItem,ChartItemAdmin)
admin.site.register(Sampler,SamplerAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Shipping,ShippingAdmin)


