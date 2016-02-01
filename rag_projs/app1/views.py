#from django.shortcuts import render
from django.http import HttpResponse
import test_view
import json, re

def display(request):
    req_info = map(lambda x:str(x.strip()), str(request).split(',')[:])
    res_ar = []
    res_ar += [' : '.join(map(str, x)) for x in sorted(request.META.items(), key=lambda x:x[0])]
    tmp_ar = []
    for x in req_info:
        if re.search(':{', x):
           if tmp_ar:
               res_ar.append(', '.join(tmp_ar))
           tmp_ar = [x]
           continue
        if not tmp_ar:
           res_ar.append(x)
        elif '}' in x:
           tmp_ar.append(x)
           res_ar.append(', '.join(tmp_ar))
           tmp_ar = []
        else:
           tmp_ar.append(x)
    return HttpResponse('<hr><br>'.join(res_ar))
    #print '<br><br>RAG<br><br>'
    res_ar = []
    res_ar += [request.path]
    res_ar += [request.get_host()]
    res_ar += [request.get_full_path()]
    res_ar += [str(request.is_secure())]
    res_ar += req_info[:]
    #res_ar = [str(request.META)]
    return HttpResponse('<hr><br>'.join([x for x in res_ar if 1 or x[2:6] == 'META']))
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
