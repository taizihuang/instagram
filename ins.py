import os,requests,json,datetime
from bs4 import BeautifulSoup
from mako.template import Template
os.environ['https_proxy']='127.0.0.1:7890'

def fetchComment(id):
    doc = json.loads(requests.get('https://i.instagram.com/api/v1/media/{}/comments/?can_support_threading=true&permalink_enabled=false'.format(id),headers=headers).content)
    comments = doc['comments']
    comment_list = []
    for comment in comments:
        comment_list.append(comment['text'])
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

def fetchIns(headers):

    with open('latest.txt','r') as f:
        c = f.read()
    url = "https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables=%7B%22id%22%3A%223127941626%22%2C%22first%22%3A12%7D"
    docu = requests.get(url,headers=headers).content
    doc = json.loads(docu)
    data = []
    edge = doc['data']['user']['edge_owner_to_timeline_media']['edges']
    for i in range(len(edge)):
        node = edge[i]['node']
        code = node['shortcode']
        id = node['id']
        if i == 0:
            if code == c:
                quit()
            else:
                with open('latest.txt','w') as f:
                    f.write(code)
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
        comment_list = fetchComment(id)
        comment = '<br>->  '.join(comment_list)
        t = datetime.datetime.fromtimestamp(node['taken_at_timestamp']).strftime('%Y/%m/%d')
        data.append((url,t,caption,comment))
    genHTML(data)

headers = {
    'cookie': 'mid=YF4JlwALAAHD4x9uS3EtNR5NBAx4; ig_did=97E920C4-AFDC-4DA4-A334-EE8552DE27B2; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; csrftoken=FsmuOqR2bm54Ald6RfkEEXaNM6Tyudd7; ds_user_id=52459994591; sessionid=52459994591%3Aopj0twpgSuw2VH%3A14;',
    'x-asbd-id': '198387',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR2lgwQ6fzk9KaZ6pqsMi664cQMX8-j7byYt2qklbPTp4Yhq',
    'origin': 'https://www.instagram.com',
    'referer': 'https://www.instagram.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
}
fetchIns(headers)