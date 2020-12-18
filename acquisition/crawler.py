from sys import argv
import requests as rq
import json
from time import sleep, time

jsonp = "112407385560764157901_1587084031775"


def crawl(titleId, filename=None, length=15, sort_q="BEST"):
    if filename is None:
        filename = titleId
    error_stock = 1
    with open(f"{filename}.json", 'w', encoding='utf-8') as out:
        all_comments = []
        no = 0
        while error_stock >= 0:
            no += 1
            # comment_url = f'comic.naver.com/comment/comment.nhn?titleId={titleId}&no={no}'
            u = f'http://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=comic&templateId=webtoon&pool=cbox3&_callback=jQuery{jsonp}&lang=ko&country=KR&objectId={titleId}_{no}&categoryId=&pageSize=100&indexSize=10&groupId=&listType=OBJECT&sort={sort_q}&_=1489937311112'
            comment_url = f"{u}&page=1"
            header = {
                "Host": "apis.naver.com",
                "Referer": f"http://comic.naver.com/comment/comment.nhn?titleId={titleId}&no={no}",
                "Content-Type": "application/javascript",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.53"
            }

            res = rq.get(comment_url, headers=header)
            text = res.content.decode('utf-8')
            obj = json.loads(text[7 + len(jsonp):-2])
            if not obj["success"]:
                raise Exception("Access Failure")
            comments = obj["result"]["commentList"]
            if len(comments) == 0:
                print(f"No comment at {titleId}:{no}.")
                error_stock -= 1
                continue
            else:
                error_stock = 1
            all_comments.append(list(map(lambda el: {"contents": el["contents"], "regTime": el["regTime"]}, comments)))
            sleep(0.01)

        out.write(json.dumps(all_comments, ensure_ascii=False))
        print(f"Wrote {len(all_comments)} lines at {filename}.json")


if __name__ == "__main__":
    ini = time()
    if len(argv) == 1:
        print("Usage: replies.py titleId [filename]; try 20853 SoundOfMind")
        # crawl(20853,1222) 마소

    elif len(argv) == 2:
        crawl(argv[1])
    elif len(argv) >= 3:
        crawl(argv[1], argv[2])
    print(time() - ini)
