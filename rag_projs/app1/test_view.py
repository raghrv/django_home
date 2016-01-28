#!usr/bin/python
#!-*- coding:utf-8 -*-

class ttest(object):
    def __init__(self, i, n):
        self.i = i
        self.n = n

    def test_view_rep(self):
        req_info = str(self.n).split(',')
        with open('rag_http_req_info.txt', 'w') as fp:
            try:
                fp.write('\n'.join(req_info))
            except:
                return '<br>'.join(req_info)
        return self.i * self.n

if __name__=='__main__':
    obj = ttest(4, 'rag')
    print obj.test_view_rep()
