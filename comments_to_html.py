"""
将评论列表转为单页html
依赖: Jinja2
"""
from jinja2 import Template


class Comment:
    def __init__(self, name, sex=None, time=None, like=0, content=None, location=None, uid=None):
        self.name = name
        self.sex = sex
        self.time = time
        self.like = like
        self.content = content
        self.location = location
        self.uid = uid

class RootComment:
    def __init__(self, id, comment, child_comments, score):
        self.id = id
        self.comment = comment
        self.child_comments = child_comments
        self.score = score

    
def root_comments_to_html(root_comments, out_path):
    template = Template(html_template)
    rendered_html = template.render(comments=root_comments)
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
    }
    .user {
      color: #61666d;
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
      color: #9499a0;
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
      color: #9499a0;
    }
  </style>
</head>
<body>

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
            {% if comment.like != None -%}
               👍 {{ comment.like }}  
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
                        <div class="child-comment">
                                <span class="user">{{ child_comment.name }}:</span> <span>{{ child_comment.content }}</span>
                                <div class="comment-meta">
                                    {% if child_comment.time != None -%}
                                        {{ child_comment.time }}  
                                    {% endif -%}
                                    {% if child_comment.location != None -%}
                                       IP属地: {{ child_comment.location }}  
                                    {% endif -%}
                                    {% if child_comment.like != None -%}
                                       👍 {{ child_comment.like }}  
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
  </script>
</body>
</html>
"""

    
def main():
    json_path = '/home/v/Downloads/test.json'
    out_path = 'out.html'
    
    import json
    root_comments = json.load(json_path)
    root_comments_to_html(root_comments, out_path)

if __name__ == "__main__":
    main()

