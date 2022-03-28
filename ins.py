import os,requests,json,datetime
from bs4 import BeautifulSoup
from mako.template import Template

def fetchComment(code):
    doc = json.loads(requests.get('https://www.instagram.com/p/{}/?__a=1&__d=dis'.format(code)).content)
    edges = doc['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
    comment_list = []
    for i in range(len(edges)):
        comment_list.append(edges[i]['node']['text'])
    return comment_list
def fetchMedia(url,code):
    if type(url) == str:
        img = requests.get(url).content
        if 'mp4' in url:
            url = code+'.mp4'
        else:
            url = code+'.jpg'
        imgfile = './media/'+url
        with open(imgfile,'wb') as f:
            f.write(img)
    else:
        for i in range(len(url)):
            img = requests.get(url[i]).content
            url[i] = code+'_'+str(i)+'.jpg'
            imgfile = "./media/"+url[i]
            with open(imgfile,'wb') as f:
                f.write(img)
    return url

def genHTML(data):
    HTML = Template("""<!DOCTYPE html><html><head>
    <meta content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no" name=viewport><meta charset=utf-8>
    <meta name="referrer" content="no-referrer">
    <link rel="stylesheet" href="./init.css">
    <title>News</title>
    </head>
    <body><div class="BODY">
    <h3>更新时间：${time}</h3>
    <div class="REPLY_LI">
    %for url,t,caption,comment in data:
    <div class="LI">
    <div class="REPLY"><strong>${caption}</strong><br>
    %if type(url)==list:
    %for pic in url:
    <img id="myImg" loading="lazy" src=./media/${pic} onclick="click1(this.src)" width=auto height="100">
    %endfor
    %elif 'jpg' in url:
    <img id="myImg" loading="lazy" src=./media/${url} onclick="click1(this.src)" width=auto height="100">
    %else:
    <video class="quote_video" src=./media/${url}  width=auto height="240" controls="controls"></video>
    %endif
    </div>
    <div class="SAY">${comment}</br></div>
    <div class="TIME">${t}</div>
    </div>
    %endfor
    <div id="myModal" class="modal">
    <span class="close" onclick="click2()">&times;</span>
    <img class="modal-content" id="img01"></div>
    <script src="init.js"></script>
    </body></html>""")

    time = datetime.datetime.now().strftime('%m-%d %H:%M')
    with open('index.html','w',encoding='utf8') as html:
        html.write(HTML.render(data=data,time=time))
url = 'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables=%7B%22id%22%3A%223127941626%22%2C%22first%22%3A12%7D'
doc = json.loads(requests.get(url).content)
data = []
edge = doc['data']['user']['edge_owner_to_timeline_media']['edges']
for i in range(len(edge)):
    node = edge[i]['node']
    code = node['shortcode']
    url = node['display_resources'][-1]['src']
    if 'edge_sidecar_to_children' in node:
        url = [url]
        edges = node['edge_sidecar_to_children']['edges']
        for e in edges:
            url.append(e['node']['display_resources'][-1]['src'])
    if 'video_url' in node:
        url = node['video_url']
    caption = ''
    if node['edge_media_to_caption']['edges']:
        caption = node['edge_media_to_caption']['edges'][0]['node']['text']
    url = fetchMedia(url,code)
    comment_list = fetchComment(code)
    comment = '<br>->  '.join(comment_list)
    t = datetime.datetime.fromtimestamp(node['taken_at_timestamp']).strftime('%Y/%m/%d')
    data.append((url,t,caption,comment))
genHTML(data)
