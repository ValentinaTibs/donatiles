from django.contrib import admin
from CRM.models import Profile, Chart, ChartItem

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    #list_display = ('user.email')

class ChartItemAdmin(admin.ModelAdmin):
    model = ChartItem


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

	list_display = ('session_id','completion_status','order_status','is_sample','created_at','modified_at','_num_prods')
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