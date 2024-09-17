
import datetime

def timestamp_to_str(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

        
def sum_list(objs, prop, default=0):
    if not objs:
        return default
    return sum(getattr(obj, prop) for obj in objs)
    

# 计算评论热度来决定排名, 建议保留原csv/json等数据文件, 以便在修改计算规则后重新生成html
def calc_root_comment_score(root_comment):
    comment = root_comment.comment
    child_comments = root_comment.child_comments
    return calc_score(like=comment.like, dislike=comment.dislike, child_like=sum_list(child_comments, 'like', 0), child_dislike=sum_list(child_comments, 'dislike', 0), child_cnt=(0 if not child_comments else len(child_comments)))

def calc_score(like=0, dislike=0, child_cnt=0, child_like=0, child_dislike=0):
    return like*2 + dislike*2 + child_cnt*3 + child_like*2 + child_dislike*2

def fill_reply_at(root_comment):
    child_comments = root_comment.child_comments
    if not child_comments:
        return
    
    child_comments_dict = {i.id: i for i in child_comments}
    
    for comment in child_comments:
        to = comment.reply_to
        if to:
            reply_to = child_comments_dict.get(to)
            if reply_to:
                reply_name = reply_to.name
            else:
                reply_name = '[内容已删除]'
            comment.content = f'回复 @{reply_name}: {comment.content}'
    