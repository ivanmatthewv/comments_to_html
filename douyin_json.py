"""
抖音评论转为转为单页html

依赖: https://greasyfork.org/zh-CN/scripts/491785 (保存fetch和xhr) 生成的savedResponse_<datetime>.json

js修改:
添加match:
// @match        https://www.douyin.com/*
添加newFunction:
newFunction("https://www-hj.douyin.com/aweme/v1/web/comment/list/*");
newFunction("https://www-hj.douyin.com/aweme/v1/web/comment/list/reply/*");

保存的数据有问题时可以把设值取值方法GM_setValue(response.url, jsonString);和keys = GM_listValues();...用全局对象如var data = {}替换
"""

import json

from comments_to_html import Comment, RootComment, root_comments_to_html
from util import timestamp_to_str, distinct_list, group_list


def json_to_root_comments(f_path, out_path, url=None, title='在线页面'):
    with open(f_path, 'r') as f:
        data = json.load(f)
        
    root_datas = []
    child_datas = []
    
    for data_url, data in data.items():
        if data_url.startswith('https://www-hj.douyin.com/aweme/v1/web/comment/list/?'):
            root_datas = root_datas + data['comments']
            continue
        if data_url.startswith('https://www-hj.douyin.com/aweme/v1/web/comment/list/reply/?'):
            child_datas = child_datas + data['comments']
                
    # 去重 有重复现象(url太长和复杂)
    root_datas = distinct_list(root_datas, 'cid')
    child_datas = distinct_list(child_datas, 'cid')
    
    child_datas_dict = group_list(child_datas, 'reply_id')
    
    root_comments = []
    for root_data in root_datas:
        id = root_data['cid']
        group_child_datas = child_datas_dict.get(id)
        if group_child_datas:
            root_data['child_comments'] = group_child_datas
    
        root_comment = root_data_to_root_comment(root_data)
        root_comments.append(root_comment)
    root_comments_to_html(root_comments, out_path, url, title)
    
def root_data_to_root_comment(data):
    comment = data_to_comment(data)
    child_datas = data.get('child_comments')
    if child_datas:
        child_comments = [data_to_comment(i) for i in child_datas]
    else:
        child_comments = None
        
    root_comment = RootComment(id=data['cid'], comment=comment, child_comments=child_comments)
    return root_comment

def data_to_comment(data):
    user = data['user']
    
    content = data.get('text')
    if not content:
        content = ''
    sticker = data.get('sticker')
    image_list = data.get('image_list')
    if sticker:
        content = f'{content}[表情]'
    if image_list:
        content = f'{content}[图片]'
        
    comment = Comment(
        id=data.get('cid'),
        name=user.get('nickname'),
        content=content,
        time=timestamp_to_str(data.get('create_time')),
        like=int(data.get('digg_count')),
        location=data.get('ip_label'),
        uid=user.get('uid'),
        reply_to=data.get('reply_to_username'),
        reply_to_uid=data.get('reply_to_userid'),
        reply_to_reply_id=data.get('reply_to_reply_id'),
    )
    return comment


def main():
    f_path = '1.json'
    out_path = 'out.html'
    json_to_root_comments(f_path, out_path)
    pass

if __name__ == "__main__":
    main()
