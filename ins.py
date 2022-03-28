import os,requests,json,datetime
from bs4 import BeautifulSoup
from mako.template import Template

def fetchComment(code):
    headers={
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
}
    doc = json.loads(requests.get('https://www.instagram.com/p/{}/?__a=1&__d=dis'.format(code),headers=headers).content)
    edges = doc['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
    comment_list = []
    for i in range(len(edges)):
        comment_list.append(edges[i]['node']['text'])
    return comment_list
def fetchMedia(url,code):
    headers={
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
}
    if type(url) == str:
        img = requests.get(url,headers=headers).content
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
url = "https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables=%7B%22id%22%3A%223127941626%22%2C%22first%22%3A12%7D"
headers={
    'Host': 'www.instagram.com',
    'Origin': 'https://www.instagram.com',
    'upgrade-insecure-requests': '1',
    'cookie': 'mid=YF4JlwALAAHD4x9uS3EtNR5NBAx4; ig_did=97E920C4-AFDC-4DA4-A334-EE8552DE27B2; fbm_124024574287414=base_domain=.instagram.com; ig_nrcb=1; csrftoken=FsmuOqR2bm54Ald6RfkEEXaNM6Tyudd7; ds_user_id=52459994591; sessionid=52459994591%3Aopj0twpgSuw2VH%3A14; fbsr_124024574287414=-GVt73f_-cpmp-MaSz2iLsBlikW9E6niK0K4NMNkjk8.eyJ1c2VyX2lkIjoiMTAwMDA2NTUzNTcyODE1IiwiY29kZSI6IkFRQlNZNk5BVk14TUR6UmNTU3JjclI3N3k5dTZ0QnZFandtTzJod1pYWUNoc1liMFJGbzB0TFFBRERLOEE5UUZkNWJFejNrUm5fNTBBOXpsVTN0WEQ2aHc3cDFrY0RCdHQ5SUJkQldtazVNQk05YXJyWTRYYjh4WEt5MFl5eDhROWFWN1RqVUdKZHpUUnFYVkQwbTR3UFlmREVuX05CeXZzOURMendINFpFalBMYUlyQUtGNUVpeVkxZHc2NzNKdERHRWZXWjRXalEyVVp2NzgtVV8xVG9fMUwyejMyQzBqdFFwa1VpazNobjF2dE5IZ1NNMVlheDNDaVQ5Q0t2TXpUTnp2V2FFeVpEM0E0S0pjc3B5Z1NRZllhX0I1eFJ1dlFMemNfMUFjWGRKY1pEN2piUWdJOUZrLS1pMlhyRXhaWS1INE9SWEQ1VjdYbGdyTVNUUE1rNEQ5Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUtjbEFINm9yOU1XaVVLd1RLeGFVZUlma0JsR1dRbkNycVh5aXFJZ1VIMHBNcDVqbGdUSklDT3JVWkJBQ2JpcnFHbEdRM2JMMGYxOWFGTTl3eEF5UXV6NWU0cGZaQzdIV0pVUEtaQlJ2ZHRwMkFhbndOaWFZd2ZCUGlSQkt5NG8zWkNCTVBJZ1hTWDBaQ0JzVDhaQnhCbE9ra211QlBrQ3FTQjdkRnRxb29UTTFNYTdjV1JGWVpEIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE2NDg0NTE4NTB9; rur="NAO\05452459994591\0541679989053:01f78f8017555a60545b0a393a1727b4ceef94779fe03ce2c2f9fc3d9b157729c0c75f5d"',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10156) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15'
}
docu = requests.get(url,headers=headers).content
print(docu)
doc = json.loads(docu)
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
