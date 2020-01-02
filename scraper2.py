# coding:utf-8

import datetime
import codecs
import requests
import os
import time
from pyquery import PyQuery as pq


def git_add_commit_push(date, filename):
    cmd_git_add = 'git add {filename}'.format(filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)


def createMarkdown(date, filename):
    with open(filename, 'w') as f:
        f.write("## " + date + "\n")


def scrape(language, filename):
    f0 = open('list.md','a')
    sinces = ['daily','weekly','monthly']
    spokens = ['en','zh']
    
        

    keywords = ['deep-learning',
            'machine-learning',
            'reinforcement-learning',
            'nlp',
            'natural-language-processing',
            'natural-language-understanding',
            'pytorch',
            'tensorflow',]

    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8'
    }

    with codecs.open(filename, "a", "utf-8") as f:
        # codecs to solve the problem utf-8 codec like chinese
        f.write('\n#### {language}\n'.format(language=language))
        strdate2 = datetime.datetime.now().strftime('%Y-%m')
        filename2 = '{date}.md'.format(date=strdate2)
        f2 = codecs.open(filename2,"a","utf-8")
        f2.write('\n#### {language} - {strdate}\n'.format(language=language,strdate=filename[:-3]))

        for since in sinces:
            for spoken in spokens:
                with open('list.md','r') as f1:
                    lists = f1.readlines()

                url = 'https://github.com/trending/{language}?since={since}&spoken_language_code={spoken}'.format(language=language,since=since,spoken=spoken)
                r = requests.get(url, headers=HEADERS)
                assert r.status_code == 200

                # print(r.encoding)
                d = pq(r.content)
                items = d('div.Box article.Box-row')
                # print(len(items))

                for item in items:
                    i = pq(item)
                    title = i(".lh-condensed a").text()
                    owner = i(".lh-condensed span.text-normal").text()
                    description = i("p.col-9").text()
                    url = i(".lh-condensed a").attr("href")
                    url = "https://github.com" + url
                    total_star = i("a.muted-link").text().split(' ')
                    today_star = i("span.float-sm-right").text()

                    r2 = requests.get(url,headers=HEADERS)
                    assert r2.status_code ==200
                    d = pq(r2.content)
                    it = d('div.repository-topics-container')

                    #if (True in map(lambda x:x in str(pq(it).text()),keywords)) and \
                    #        (title+'\n' not in lists) and \
                    #        ('framwork' not in str(pq(it).text())):
                    if title+'\n' not in lists:
                        try:
                            f.write(u"* [{title}]({url}):{description}\n{today_star}/{total_star} total stars, {total_forks} total forks.\n".format(title=title, url=url, description=description,today_star = today_star,total_star=total_star[0],total_forks=total_star[1]))
                            f2.write(u"* [{title}]({url}):{description}\n{today_star}/{total_star} total stars, {total_forks} total forks.\n".format(title=title, url=url, description=description,today_star = today_star,total_star=total_star[0],total_forks=total_star[1]))
                            strdate2 = datetime.datetime.now().strftime('%Y-%m')
                            f0.write("{title}\n".format(title=title))
                        except:
                            pass
            
                    # print(str(pq(it).text()),'\nKeyword matches:',True in map(lambda x:x in str(pq(it).text()),keywords),'\nNew item:',(title+'\n' not in lists),'\n\n')
    f0.close()
    f2.close()
    git_add_commit_push(strdate2,filename2)

def job():

    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    # create markdown file
    createMarkdown(strdate, filename)

    # write markdown
    scrape('python', filename)
    scrape('Jupyter Notebook',filename)
    scrape('C++',filename)
    scrape('Java',filename)
    
    scrape('swift', filename)
    scrape('javascript', filename)
    scrape('go', filename)

    # git add commit push
    git_add_commit_push(strdate, filename)
    print('Finish')


if __name__ == '__main__':
    while True:
        #try:
        job()
        #except:
         #   pass
        time.sleep(24 * 60 * 60)
