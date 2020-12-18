# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import argv
import json
from time import sleep
import urllib.request as req


def crawl(titleId, filename=None, stock=1):
    if filename is None:
        filename = titleId
    error_stock = stock
    driver = webdriver.Edge("msedgedriver.exe")
    all_comments = []
    i = 0
    while error_stock >= 0:
        i += 1
        driver.get(f"https://comic.naver.com/comment/comment.nhn?titleId={titleId}&no={i}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        comments = soup.select(
            '#cbox_module > div > div.u_cbox_content_wrap > ul > li.u_cbox_comment > div.u_cbox_comment_box > div > div.u_cbox_text_wrap > span.u_cbox_contents')
        if len(comments) == 0:
            print(f"No comment at {titleId}:{i}.")

            error_stock -= 1
            continue
        else:
            error_stock = stock
        all_comments.append(list(map(lambda el: el.string, comments)))
    with open(f"{filename}.json", 'w', encoding='utf-8') as out:
        out.write(json.dumps(all_comments, ensure_ascii=False))
        print(f"Wrote {len(all_comments)} lines.")


if __name__ == "__main__":
    if len(argv) == 1:
        print("Usage: replies.py titleId [filename]; try 20853 SoundOfMind")
        # crawl(20853,1222) 마소

    elif len(argv) == 2:
        crawl(argv[1])
    elif len(argv) >= 3:
        crawl(argv[1], argv[2])
