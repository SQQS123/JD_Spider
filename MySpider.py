# coding=utf8
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


cate_url = "https://list.jd.com/list.html?cat=9987,653,655"
cate_response = get_http_response(cate_url)

# 打开浏览器，为了价格
index = 0
browser = webdriver.PhantomJS()
browser.get(cate_url)
price = browser.find_elements_by_xpath("//strong[@class='J_price']")

# print(cate_response.text)
if cate_response.status_code == 200:
	goods = {}
	bs_obj = bs(cate_response.text, 'html.parser')
	box_list = bs_obj.select('li.gl-item')
	# 这样我们就直接得到了所有的商品的栏目
	for box in box_list:
		# print(box)
		
		# 得到商品详情页的完整url
		info_url ='https:' + box.select_one("a").attrs["href"]
		goods['info_url'] = info_url
		print("商品详情:"+info_url)
		
		# 得到这个对象的一些方法,相当于help(obj),编程看手册
		# print(dir(box.select_one("img")))
		# 得到图片的完整路径
		# 其实下面的代码不够强壮
		if box.select_one("img").has_attr("src"):
			img_url = box.select_one("img").attrs["src"]
		else:
			img_url = box.select_one("img").attrs["data-lazy-img"]
		img_url = 'https:' + img_url
		goods['img_url'] = img_url
		print("图片链接:"+img_url)
		
		# 得到商品的标题
		# 通过选择em得到标题的em的序号，然后选择它
		title = box.select("em")[2].text.strip()
		goods['title'] = title
		print("商品标题:"+title)
		
		# 得到商品的价格,我打算用selenium
		# 通过打开PhantomJS浏览器得到
		goods['price'] = price[index].text
		print("商品价格"+price[index].text)
		
		# 如果下面不加'utf-8'的话会报错,报错内容大概是下面的
		# 某个gbk无法解码
		# 所以解决方式就是加encoding='utf-8'和ensure_ascii=False
		# json.dumps序列化时默认使用的ascii编码，想输出真正的中文需要指定ensure_ascii=False
		# 而将文件写入时默认使用的是gbk，所以我们需要encoding='utf-8'
		with open('f:\\JD\\jd_goods.txt','a',encoding='utf-8') as f:
			f.writelines(json.dumps(goods,ensure_ascii=False) + '\n')
		index += 1