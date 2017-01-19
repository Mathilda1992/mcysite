from django.contrib import admin
from .models import Blog,Person,Publisher,Book,Author2
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','author','pub_date','update_time',)
    search_fields = ('author','pub_date',)
    list_filter = ('author','pub_date',)


    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        # handle something here
        obj.delete()




class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name','age',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PersonAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct




class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self,request):
        qs = super(MyModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author = request.user)



class BookAdmin(admin.ModelAdmin):
    list_display = ('title','publisher','publication_date')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    filter_horizontal = ('authors',)
    raw_id_fields = ('publisher',)

admin.site.register(Blog,BlogAdmin)
admin.site.register(Person)

admin.site.register(Publisher)
admin.site.register(Author2)
admin.site.register(Book,BookAdmin)