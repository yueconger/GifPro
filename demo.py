# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2020/5/17 22:27
@Author  : yuecong
@Email   : yueconger@163.com
@Software: PyCharm
"""
import re
html = """
 <li class="page-item active" aria-current="page"><span class="page-link">1</span></li>
                                                                                <li class="page-item"><a class="page-link" href="/article/list/?page=2">2</a></li>
                                                                                <li class="page-item"><a class="page-link" href="/article/list/?page=3">3</a></li>
                                                                                <li class="page-item"><a class="page-link" href="/article/list/?page=4">4</a></li>
                                                                                <li class="page-item"><a class="page-link" href="/article/list/?page=5">5</a></li>
                                                                                <li class="page-item"><a class="page-link" href="/article/list/?page=6">6</a></li>
                                                                                <li class="page-item"><a class="page-link" href="/article/list/?page=7">7</a></li>
                                                                                <li class="page-item"><a class="page-link" href="/article/list/?page=8">8</a></li>
                                                                    
                            <li class="page-item disabled" aria-disabled="true"><span class="page-link">...</span></li>
            
            
                                
            
            
                                                                        <li class="page-item"><a class="page-link" href="/article/list/?page=2181">2181</a></li>
                                                                                <li class="page-item"><a class="page-link" href="/article/list/?page=2182">2182</a></li>
                                                        
        
                    <li class="page-item">
                <a class="page-link" href="/article/list/?page=2" rel="next" aria-label="Next &raquo;">&rsaquo;</a>
            </li>"""

# pattern = 'href="/article/list/\?page=(\d+)".*?\nhref="/article/list/\?page=2" rel="next"'
# res = re.findall(pattern, html)
# print(res)
tag_list = ['cccccc']
str = "aa   bbbbb         ccc  d"
str_list = str.split()
tag_list.extend(str_list)
print(len(tag_list))
print(tag_list)
tag_list = ['你好']
if len(tag_list) > 1:
    tag = "、".join(tag_list)
elif len(tag_list) == 1:
    tag = tag_list[0]
else:
    tag = ''
print(tag)

# url = "http://img.doutula.com/production/uploads/image/2020/05/14/20200514440626_caHOJw.gif"
# import hashlib
# obj = hashlib.md5()
# print(obj)
# obj.update(bytes(url, encoding='utf-8'))
# name = obj.hexdigest()
# print(name)
# nn = url.split('/')[-1].split('.')[-1]
# print(nn)
tag_list = ["aaa"]

mmm = 'aaa'
a = mmm.split()
print(a)