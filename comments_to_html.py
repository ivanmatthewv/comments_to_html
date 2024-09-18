"""
将评论列表转为单页html
依赖: Jinja2
"""
import operator

from jinja2 import Template

from util import sum_list


class Comment:
    def __init__(self, id=None, name=None, sex=None, time=None, like=0, dislike=0, content=None, location=None, uid=None, reply_to=None, reply_to_uid=None, reply_to_reply_id=None):
        self.id = id
        self.name = name
        self.sex = sex
        self.time = time
        self.like = like
        self.dislike = dislike
        self.content = content
        self.location = location
        self.uid = uid
        """
        以下仅要回复二级评论的评论对象使用
        reply_to: 要回复的用户名
        reply_to_uid: 要回复的用户id
        reply_to_reply_id: 要回复的二级评论id
        """
        self.reply_to = reply_to
        self.reply_to_uid = reply_to_uid
        self.reply_to_reply_id = reply_to_reply_id
        

class RootComment:
    def __init__(self, id=None, comment=None, child_comments=None, score=None):
        self.id = id
        self.comment = comment
        self.child_comments = child_comments
        self.score = score

    
def root_comments_to_html(root_comments, out_path, url=None, title='在线页面'):
    root_comments = sort_root_comments(root_comments)
  
    template = Template(html_template)
    rendered_html = template.render(comments=root_comments, url=url, title=title)
    with open(out_path, 'w') as f:
        f.write(rendered_html)

html_template = """
<!DOCTYPE html>
<html>
<head>
  <title>comments</title>
  <style>
    body {
      font-family: sans-serif;
      color: #18191c;
    }
    .title {
      text-align: center;
    }
    .root-comment-container {
      margin-bottom: 36px;
    }
    .root-comment-content {
      margin-top: 5px;
    }
    .comment-meta {
      margin-top: 6px;
      font-size: smaller;
    }
    .child-comments-container {
    }
    .child-comment {
      margin-left: 20px;
      padding: 16px 0px 0px 34px;
    }
    .show-more-content {
      cursor: pointer;
      margin-left: 20px;
      padding: 8px 0px 0px 34px;
      font-size: smaller;
    }
    
    .title a {
      color: #61666d;
    }
    .user {
      color: #61666d;
    }
    .comment-meta {
      color: #9499a0;
    }
    .show-more-content {
      color: #9499a0;
    }
    
    @media (prefers-color-scheme: dark) {
      body {
        background-color: black;
        color: #d8d4cf;
      }
    }
  </style>
</head>
<body>

  {% if url != None -%}
    <h3 class="title"><a target="_blank" href="{{ url }}">{{ title }}</a></h3>
  {% endif -%}
  
  <div id="root-comments"> <!-- 1 -->
    {% for root_comment in comments %}
      {% set comment = root_comment.comment %}
      <div class="root-comment-container"> <!-- 2 -->
        <div class="root-comment-content"><span class="user">{{ comment.name }}:</span> <span>{{ comment.content }}</span></div>
        <div class="comment-meta">
            {% if comment.time != None -%}
                {{ comment.time }}  
            {% endif -%}
            {% if comment.location != None -%}
               IP属地: {{ comment.location }}  
            {% endif -%}
            {% if comment.like != None and comment.like > 0 -%}
               👍 {{ comment.like }}  
            {% endif -%}
            {% if comment.dislike != None and comment.dislike > 0 -%}
               👎🏼 {{ comment.dislike }}  
            {% endif -%}
            {% if comment.sex != None -%}
               性别: {{ comment.sex }}  
            {% endif -%}
            {% if comment.uid != None -%}
               ID: {{ comment.uid }}  
            {% endif -%}
        </div>
        
         {% if root_comment.child_comments != None -%}
            <div class="child-comments-container"> <!-- 3 -->
              
              <div class="child-comments"> <!-- 4 -->
                  {% for child_comment in root_comment.child_comments %}
                        <div class="child-comment" child_comment_id="{{ child_comment.id }}">
                                <span class="user">{{ child_comment.name }}:</span> 
                                {% if child_comment.reply_to != None -%}
                                    <span class="child-comment-reply">
                                        <abbr class="reply-abbr" 
                                        {% if child_comment.reply_to_reply_id != None -%}
                                          reply_to_reply_id="{{ child_comment.reply_to_reply_id }}" 
                                        {% endif -%}
                                        {% if child_comment.reply_to_uid != None -%}
                                          reply_to_uid="{{ child_comment.reply_to_uid }}" 
                                        {% endif -%}
                                        title="">回复 @{{ child_comment.reply_to }}:</abbr> 
                                    </span>
                                {% endif -%}
                                <span class="child-comment-content">{{ child_comment.content }}</span>
                                <div class="comment-meta">
                                    {% if child_comment.time != None -%}
                                        {{ child_comment.time }}  
                                    {% endif -%}
                                    {% if child_comment.location != None -%}
                                       IP属地: {{ child_comment.location }}  
                                    {% endif -%}
                                    {% if child_comment.like != None and child_comment.like > 0 -%}
                                      👍 {{ child_comment.like }}  
                                    {% endif -%}
                                    {% if child_comment.dislike != None and child_comment.dislike > 0 -%}
                                      👎🏼 {{ child_comment.dislike }}  
                                    {% endif -%}
                                    {% if child_comment.sex != None -%}
                                       性别: {{ child_comment.sex }}  
                                    {% endif -%}
                                    {% if child_comment.uid != None -%}
                                       ID: {{ child_comment.uid }}  
                                    {% endif -%}
                                </div>
                          </div>
                    {% endfor %}
                </div>  <!-- 4 -->
                 
                 
                {% set child_comment_cnt = root_comment.child_comments | count %}
                {% if child_comment_cnt > 3 -%}
                  <div class="show-more-content" data-id="{{ root_comment.id }}">
                        <span>共 {{ child_comment_cnt }}  条回复</span>
                        <span class="show-more">查看更多</span>
                        <span class="show-more-recovery">收起</span>
                  </div>
                {% endif -%}
                
            </div> <!-- 3 -->
        {% endif -%}
      </div> <!-- 2 -->
    {% endfor %}
  </div> <!-- 1 -->

  <script>
        function scrollToPrevElement(el) {
            el.scrollIntoView({
                behavior: 'smooth', // 平滑滚动
                block: 'nearest',   // 尽量滚动到最近的可视区域
                inline: 'nearest'
            });
        }
        
        function show_more(el) {
            var parent = el.parentNode;  
            var recovery_btn = Array.from(parent.children).find(sibling => sibling.classList.contains('show-more-recovery'));
            
            var siblings = Array.from(parent.parentNode.children);  
            var siblingWithClassB = siblings.find(sibling => sibling.classList.contains('child-comments'));
            if (siblingWithClassB) {
                var children = siblingWithClassB.children
                if (children && children.length) {
                    var cnt = 0;
                    var i = 0;
                    for (; i < children.length; i++) {
                        child = children[i];
                        if (child.style.display == 'none') {
                            child.style.display = '';
                            cnt = cnt + 1;
                            if (cnt >= 10) {
                                break;
                            }
                        }
                    }
                    if (recovery_btn) {
                        recovery_btn.style.display = '';
                    }
                    if (i >= children.length - 1) {
                        el.style.display = 'none'
                    }
                }
            }
        }
        function show_more_recovery(el) {
            var parent = el.parentNode;  
            var show_more_btn = Array.from(parent.children).find(sibling => sibling.classList.contains('show-more'));
            var siblings = Array.from(parent.parentNode.children);  
            var siblingWithClassB = siblings.find(sibling => sibling.classList.contains('child-comments'));
            
            if (siblingWithClassB) {
                var children = siblingWithClassB.children
                if (children && children.length) {
                    for (var i = 3; i < children.length; i++) {
                        child = children[i];
                        if (child.style.display != 'none') {
                            child.style.display = 'none';
                        } else {
                            break;
                        }
                    }
                    
                    el.style.display = 'none';
                    show_more_btn.style.display = '';
                    scrollToPrevElement(parent.parentNode.parentNode)
                }
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            var ele_as = document.querySelectorAll('.child-comments-container');
            ele_as.forEach(function(ele_a) {
                var ele_bs = ele_a.querySelectorAll('.child-comment');
                if (ele_bs.length > 3) {
                    for (let i = 3; i < ele_bs.length; i++) {
                        ele_bs[i].style.display = 'none';
                    }
                    ele_a.querySelector('.show-more-recovery').style.display = 'none';
                }
            });
        });
      
        document.addEventListener('click', function(event) {
          var el = event.target;
          if (el.classList.contains('show-more')) {
            show_more(el);
            return;
          }
          if (el.classList.contains('show-more-recovery')) {
            show_more_recovery(el);
            return;
          }
        }, true)
      
        document.addEventListener('mouseover', function(event) {
          var el = event.target;
          if (el.classList.contains('reply-abbr')) {
            if (el.getAttribute('title')) {
              return;
            }
            
            var reply_to_reply_id = el.getAttribute('reply_to_reply_id')
            if (reply_to_reply_id) {
              var reply_to_uid = el.getAttribute('reply_to_uid')
              reply_to_uid = reply_to_uid ? reply_to_uid + ':' : ''
              
              var reply_to = ''
              var content = `${reply_to_uid}[已删除]`
                
              selector = `div.child-comment[child_comment_id="${reply_to_reply_id}"]`;
              var target_child_comment = el.parentNode.parentNode.parentNode.parentNode.querySelector(selector);
              if (target_child_comment) {
                  var abbr_el = target_child_comment.querySelector('abbr.reply-abbr');
                  if (abbr_el) {
                      reply_to = abbr_el.innerText
                  }
                  
                  var content_el = target_child_comment.querySelector('span.child-comment-content');
                  if (content_el) {
                      content = content_el.innerText
                  }
              }
              
              content = `${reply_to}${content}`
              el.setAttribute('title', content)
            }
            return;
          }
        }, true)
  </script>
</body>
</html>
"""


def sort_root_comments(root_comments):
    for root_comment in root_comments:
        if root_comment.child_comments:
            root_comment.child_comments = sorted(root_comment.child_comments, key=operator.attrgetter('time'))
        root_comment.score = calc_root_comment_score(root_comment)
    root_comments = sorted(root_comments, key=operator.attrgetter('comment.time'))
    return sorted(root_comments, key=operator.attrgetter('score'), reverse=True)

# 计算评论热度来决定排名, 建议保留原csv/json等数据文件, 以便在修改计算规则后重新生成html
def calc_root_comment_score(root_comment):
    comment = root_comment.comment
    child_comments = root_comment.child_comments
    return calc_score(like=comment.like, dislike=comment.dislike, child_like=sum_list(child_comments, 'like', 0), child_dislike=sum_list(child_comments, 'dislike', 0), child_cnt=(0 if not child_comments else len(child_comments)))

def calc_score(like=0, dislike=0, child_cnt=0, child_like=0, child_dislike=0):
    return like*2 + dislike*2 + child_cnt*3 + child_like*2 + child_dislike*2

    
def main():
    json_path = '/home/v/Downloads/test.json'
    out_path = 'out.html'
    
    import json
    root_comments = json.load(json_path)
    root_comments_to_html(root_comments, out_path)

if __name__ == "__main__":
    main()

