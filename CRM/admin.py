from django.contrib import admin
from CRM.models import Profile, Chart, ChartItem, Shipping, Order, Sample, Sampler

class ShippingStackedAdmin(admin.StackedInline):
    model = Shipping

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    inlines = [ShippingStackedAdmin,]
    #list_display = ('user.email')

class ChartItemAdmin(admin.ModelAdmin):
    model = ChartItem
    list_display = ('chart','product','status','chart__user')

    def chart__user(self, obj):
        if obj.chart.user:
            return obj.chart.user
        else :
            return "User Non Reg"

class OrderAdmin(admin.ModelAdmin):
    model = Order
    #inlines = ('inte',)

class ShippingAdmin(admin.ModelAdmin):
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

	list_display = ('session_id','user','completion_status','created_at','modified_at','order')
	actions = [close_them]
	readonly_fields  = ( 'session_id','created_at','modified_at')
    
	inlines = [ChartItemStackedAdmin]

	def _num_prods(self, obj):
		return obj.all_items()
	_num_prods.short_description = "Number of Products"
	_num_prods.admin_order_field = 'num_prods'


class SampleStackedAdmin(admin.StackedInline):
    model = Sample

    search_fields = ('product__code', )
    readonly_fields  = ('status','modified_at')


class SamplerAdmin(admin.ModelAdmin):
	model = Sampler

    list_display = ('session_id','user','completion_status','created_at','modified_at','_num_prods','order')
	readonly_fields  = ( 'session_id','created_at','modified_at')
	inlines = [SampleStackedAdmin,'order']

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Chart,ChartAdmin)
admin.site.register(ChartItem,ChartItemAdmin)
admin.site.register(Sampler,SamplerAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Shipping,ShippingAdmin)
