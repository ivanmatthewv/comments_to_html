"""
知乎评论转为转为单页html

依赖: https://greasyfork.org/zh-CN/scripts/491785 (保存fetch和xhr) 生成的savedResponse_<datetime>.json

js修改:
修改@match为https://www.zhihu.com/*
修改newFunction值为("https://www.zhihu.com/api/v4/comment_v5/*");

保存的数据有问题时可以把设值取值方法GM_setValue(response.url, jsonString);和keys = GM_listValues();...用全局对象如var data = {}替换
"""

import json
import re

from comments_to_html import Comment, RootComment, root_comments_to_html
from util import timestamp_to_str


def json_to_root_comments(f_path, out_path):
    with open(f_path, 'r') as f:
        data = json.load(f)
        
    root_datas = []
    child_datas = {}
    
    root_comments_pattern = r"https://www.zhihu.com/api/v4/comment_v5/answers/(\d+)/root_comment(\?.*)?"
    child_comments_pattern = r"https://www.zhihu.com/api/v4/comment_v5/comment/(\d+)/child_comment(\?.*)?"            
        
    for data_url, data in data.items():
        if data_url.endswith('/config'):
            pass
        if re.match(root_comments_pattern, data_url):
            root_datas = root_datas + data['data']
            continue
        if re.match(child_comments_pattern, data_url):
            root_id = data['root']['id']
            if root_id in child_datas:
                child_datas[root_id] = child_datas[root_id] + data['data']
            else:
                child_datas[root_id] = data['data']
                
    root_comments = []
    for root_data in root_datas:
        id = root_data['id']
        c = child_datas.get(id)
        if c:
            root_data['child_comments'] = c
    
        root_comment = root_data_to_root_comment(root_data)
        root_comments.append(root_comment)
    root_comments_to_html(root_comments, out_path)
    
def root_data_to_root_comment(data):
    comment = data_to_comment(data)
    child_datas = data.get('child_comments')
    if child_datas:
        child_comments = [data_to_comment(i) for i in child_datas]
    else:
        child_comments = None
        
    root_comment = RootComment(id=data['id'], comment=comment, child_comments=child_comments)
    return root_comment

def data_to_comment(data):
    author = data['author']
    
    comment = Comment(
        id=data.get('id'),
        name=author.get('name'),
        sex=gender_to_sex(author.get('gender')),
        content=data.get('content'),
        time=timestamp_to_str(data.get('created_time')),
        like=int(data.get('like_count')),
        dislike=int(data.get('dislike_count')),
        location=process_ip(data),
        uid=author.get('id'),
    )
    
    comment = process_reply(data, comment)
    return comment

# ip
def process_ip(data):
    ip = None
    comment_tag = data.get('comment_tag')
    if comment_tag:
        ip_tag = next((d for d in comment_tag if d.get('type') == 'ip_info'), None)
        if ip_tag:
            ip = ip_tag.get('text')
    return ip

# reply @
def process_reply(data, comment):
    reply_to = None
    reply_to_uid = None
    
    reply_comment_id = data.get('reply_comment_id')
    reply_root_comment_id = data.get('reply_root_comment_id')
    if reply_comment_id and reply_comment_id != reply_root_comment_id and reply_comment_id != '0':
        reply_to_author = data.get('reply_to_author')
        if reply_to_author:
            reply_to = reply_to_author.get('name')
            reply_to_uid = reply_to_author.get('id')
        else:
            reply_to = '[内容已删除]'
            
    comment.reply_to = reply_to
    comment.reply_to_uid = reply_to_uid
    comment.reply_to_reply_id = data.get('reply_comment_id')
    return comment

def gender_to_sex(gender):
    if gender == 2:
        return '男'
    elif gender == 1:
        return '女'
    else:
        return '保密'
    

def main():
    f_path = '1.json'
    out_path = 'out.html'
    json_to_root_comments(f_path, out_path)
    pass

if __name__ == "__main__":
    main()
