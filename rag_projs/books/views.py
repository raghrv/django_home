#from django.shortcuts import render
#def search_form(request):
#    return render(request, 'search_form.html')

from django.shortcuts import render_to_response

def search_form(request):
    return render_to_response('search_form.html')
