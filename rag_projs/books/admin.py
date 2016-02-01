from django.contrib import admin
from models import Publisher, Book, Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email')
    search_fields = ('fname', 'lname')

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)



# Register your models here.
