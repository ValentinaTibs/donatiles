from django.contrib import admin
from CRM.models import Profile, Chart, ChartItem, Shipping, Order

class ShippingStackedAdmin(admin.StackedInline):
    model = Shipping

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    inlines = [ShippingStackedAdmin,]
    #list_display = ('user__username')

class ChartItemAdmin(admin.ModelAdmin):
    model = ChartItem

class OrderAdmin(admin.ModelAdmin):
    model = Order
    # list_display = ('id','profile',)

    # def profile(self, obj):
    #     return "\n".join([chart.user.username for chart in obj.charts.all()])    

    #inlines = ('inte',)

class ChartItemStackedAdmin(admin.StackedInline):
    model = ChartItem

    search_fields = ('product__publication__slug', )
    readonly_fields  = ('status','modified_at')

def close_them(modeladmin, request, queryset):
    for e in queryset:
        e.completion_status = 'cs'
        e.save() 

close_them.short_description = "Mark as Closed"

class ChartAdmin(admin.ModelAdmin):
	model = Chart

	list_display = ('session_id','user','completion_status','is_sample','created_at','modified_at','_num_prods')
	actions = [close_them]
	readonly_fields  = ( 'session_id','is_sample','created_at','modified_at')
	inlines = [ChartItemStackedAdmin,]

	def _num_prods(self, obj):
		return obj.num_prods()
	_num_prods.short_description = "Number of Products"
	_num_prods.admin_order_field = 'num_prods'

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Chart,ChartAdmin)
admin.site.register(ChartItem,ChartItemAdmin)
admin.site.register(Order,OrderAdmin)
