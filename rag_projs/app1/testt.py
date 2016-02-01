import re
import ast, json

def displayt(request):
    req_info = map(lambda x:str(x.strip()), str(request).split(',')[:])
    res_ar = []
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
    for e in res_ar:
        try:
            x1 = e.replace("'", '/"')   
            print json.loads(x1)
        except:
            pass

        print ast.literal_eval('{'+e+'}')
           
s= '''"POST":"", "COOKIES":{'csrftoken': 'wRQUsHfaKgVvIVLa9TjAP1ANl9LhaEbP', 'sessionid': 'iuy6uem6pxoey88ybzn7sk5qir21r9at'}, "META":{'COLORTERM': 'gnome-terminal', 'CONTENT_LENGTH': '', 'CONTENT_TYPE': 'text/plain', u'CSRF_COOKIE': u'wRQUsHfaKgVvIVLa9TjAP1ANl9LhaEbP', 'DISPLAY': ':0', 'DJANGO_SETTINGS_MODULE': 'rag_projs.settings', 'GATEWAY_INTERFACE': 'CGI/1.1', 'HOME': '/root', 'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate', 'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.5', 'HTTP_CONNECTION': 'keep-alive', 'HTTP_COOKIE': 'csrftoken=wRQUsHfaKgVvIVLa9TjAP1ANl9LhaEbP; sessionid=iuy6uem6pxoey88ybzn7sk5qir21r9at', 'HTTP_HOST': '127.0.0.1:8000', 'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0', 'LANG': 'en_IN', 'LANGUAGE': 'en_IN:en', 'LESSCLOSE': '/usr/bin/lesspipe %s %s', 'LESSOPEN': '| /usr/bin/lesspipe %s', 'LOGNAME': 'root', 'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lz=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.axa=00;36:*.oga=00;36:*.spx=00;36:*.xspf=00;36:', 'MAIL': '/var/mail/root', 'OLDPWD': '/django_home/rag_projs/rag_projs', 'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'PATH_INFO': u'/app1/', 'PWD': '/django_home/rag_projs', 'QT_QPA_PLATFORMTHEME': 'appmenu-qt5', 'QUERY_STRING': 'q=raghav', 'REMOTE_ADDR': '127.0.0.1', 'REMOTE_HOST': '', 'REQUEST_METHOD': 'GET', 'RUN_MAIN': 'true', 'SCRIPT_NAME': u'', 'SERVER_NAME': 'localhost', 'SERVER_PORT': '8000', 'SERVER_PROTOCOL': 'HTTP/1.1', 'SERVER_SOFTWARE': 'WSGIServer/0.1 Python/2.7.6', 'SHELL': '/bin/bash', 'SHLVL': '1', 'SUDO_COMMAND': '/bin/bash', 'SUDO_GID': '1000', 'SUDO_UID': '1000', 'SUDO_USER': 'raghav', 'TERM': 'xterm', 'TZ': 'UTC', 'USER': 'root', 'USERNAME': 'root', 'XAUTHORITY': '/home/raghav/.Xauthority', '_': '/usr/bin/python', 'wsgi.errors': ', mode 'w' at 0x7f63d95e61e0>, 'wsgi.file_wrapper': , 'wsgi.input': , 'wsgi.multiprocess': False, 'wsgi.multithread': True, 'wsgi.run_once': False, 'wsgi.url_scheme': 'http', 'wsgi.version': (1, 0)}>'''
displayt(s)
 
