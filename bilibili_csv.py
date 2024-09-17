"""
bilibili评论转为转为单页html
依赖: https://github.com/linyuye/Bilibili_crawler 生成的test_3.csv
"""

import csv
import operator

from comments_to_html import Comment, RootComment, root_comments_to_html
from util import calc_root_comment_score


class CsvRow:
    def __init__(self, column1, column2, column3, column4, column5, column6, column7, column8, column9, column10):
        comment = Comment(
            name = column1,
            sex = column2,
            time = column3.replace(' 北京时间', ''),
            like = 0 if not column4 else int(column4),
            content = column5,
            location = column6,
            uid = column9
        )
        self.comment = comment
        self.sub_cnt = 0 if not column7 else int(column7)

            
def parse_csv_to_comments(filepath):
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        return [CsvRow(*row) for row in reader]


def comments_to_root_comments(comments):
    root_comments = []
    
    idx = 0
    cnt = 0
    while True:
        row = comments[idx]
        comment = row.comment
        cnt = cnt + 1
        
        sub_cnt = row.sub_cnt
        if sub_cnt > 0:
            child_comments = comments[(idx+1):(idx+1+sub_cnt)]
            for obj in child_comments:
                assert(obj.sub_cnt == sub_cnt), f'数据sub_cnt不匹配: idx: {idx}, sub_cnt: {sub_cnt}'
            
            idx = idx + 1 + sub_cnt
            child_comments = [i.comment for i in child_comments]
            child_comments = sorted(child_comments, key=operator.attrgetter('time'))
        else:
            child_comments = None
            idx = idx + 1
            
        root_comment = RootComment(cnt, comment, child_comments)
        root_comment.score = calc_root_comment_score(root_comment)
        root_comments.append(root_comment)
        
        if idx >= len(comments):
            break
    
    return sorted(root_comments, key=operator.attrgetter('score'), reverse=True)


    
def main():
    f_path = 'test1_3.csv'
    out_path = 'out.html'
    
    comments = parse_csv_to_comments(f_path)
    root_comments = comments_to_root_comments(comments)
    root_comments_to_html(root_comments, out_path)

if __name__ == "__main__":
    main()

