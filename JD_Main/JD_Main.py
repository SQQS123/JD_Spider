import json
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from lxml import etree



DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

def get_http_response(url,params=None):
	if params is None:
		params = {}
	headers = {'user-agent': DEFAULT_USER_AGENT}
	response = requests.get(url, headers=headers, params=params)
	return response

cate_url = "https://www.jd.com/"
cate_response = get_http_response(cate_url)

if cate_response.status_code == 200:
	html = etree.HTML(cate_response.text)
	cate_lst = html.xpath("//li[@class='cate_menu_item']")
	for item in cate_lst:
		# print(item.xpath("./a/text()"))
		for i in item.xpath("./a/text()"):
			print(i)
		print('\n')