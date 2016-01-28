#from django.shortcuts import render
from django.http import HttpResponse
import test_view
import json

def display(request):
    req_info = str(request).split(',')[:6]
    #print '<br><br>RAG<br><br>'
    return HttpResponse('<br>'.join(req_info[:]))
    return HttpResponse(test_view.ttest(3, str(request)).test_view_rep())
    return HttpResponse(test_view.ttest(5, str(request) + '\n').test_view_rep())



    offset = '2'
    print '<br><br>RAG<br><br>'
    try:
        print '<br><br>RAG<br><br>'
        offset = int(offset)
    except ValueError:
        print '<br><br>RAG<br><br>'
        raise Http404()
    print '<br><br>RAG<br><br>'
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    print '<br><br>RAG<br><br>'
    assert False
    print '<br><br>RAG<br><br>'
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def get_time(request):
    import datetime
    now = datetime.datetime.now()
    html_text = '<html><body>Time : %s</body></html>' % (now)
    return HttpResponse(html_text)

# Create your views here.
