#!/usr/bin/python
#encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import requests
import json
import random
import time
#from spider import myipAgent
from send_mail import send_mail

headers = {
	'Host': 'cn.epubee.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	'X-Requested-With': 'XMLHttpRequest',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
	'Pragma': 'no-cache',
	'Cache-Control': 'max-age=0 '
}

cookie = {}

def choiceIP(ip_pool):
	ip=random.choice(ip_pool)
	proxy={'http':ip,'https':ip}
	return proxy

def getSessionid():
	login_url = u'http://cn.epubee.com'
	req = requests.get(login_url, headers=headers)
	str = req.headers['Set-Cookie']
	name, value = str.split(';')[0].split('=')
	return value

def update_cookies(data_json):
	data = (json.loads(data_json))['d'][0]
	cookie['identify'] = data.get('ID')
	cookie['identifyusername'] = data.get('UserName')
	cookie['user_localid'] = data.get('Name')
	cookie['uemail'] = data.get('email')
	cookie['kindle_email'] = data.get('kindle_email')
	cookie['isVip'] = '1'
	cookie['leftshow']='1'
	return

def getCookie(proxy):
	print(u'开始获取cookie')
	cookie['ASP.NET_SessionId'] = getSessionid()
	url = u'http://cn.epubee.com//keys/genid_with_localid.asmx/genid_with_localid'
	data = {'localid': ''}
	try:
		response = requests.post(url, json=data, cookies=cookie, proxies=proxy, timeout=10)
		if response.status_code == 200:
			update_cookies(response.content.decode())
	except Exception as e:
		print(u"获取cookie失败！")
	else :
		return response.status_code

def cookie_toString(cookie):
	cookie_str=''
	for name,vlaue in cookie.items():
		cookie_str=cookie_str+str(name)+'='+str(vlaue)+'; '
	return cookie_str

def add_Book(cookie, bookid, proxy):
	print(u'开始加入书本')
	uid = cookie.get('identify')
	cookie_str = cookie_toString(cookie)
	act = 'search'
	url = u'http://cn.epubee.com/app_books/addbook.asmx/online_addbook'
	data = {'bookid': bookid, 'uid': uid, 'act': act}
	my_header = header
	my_header['Cookie'] = cookie_str
	my_header['Connection'] = 'keep-alive'
	my_header['Content-Type'] = 'application/json'
	try:
		response = requests.post(url, headers=my_header, json=data, proxies=proxy)
		if response.status_code != 200:
			print(u'书本加入失败')
			print(u'response : %s' % response)
			print(u'req %s\ndata : %s' %(url, data))
		else:
			print(u'书本加入成功, bid=%s' % bookid)
			print(u'%s' % response.content)
	except Exception as e:
		print(u'书本加入失败')
		print(u'response : %s' % response)
		print(u'req %s\ndata : %s' %(url, data))
	return response.status_code

def getBookList(cookie,proxy):
	books = []
	print(u'开始获取书本列表')
	uid = str(cookie.get('identify'))
	url = u'http://cn.epubee.com/files.aspx?userid=' + uid
	cookie_str = cookie_toString(cookie)
	my_header = headers
	my_header['Cookie'] = cookie_str
	my_header['Referer' ] = 'http://cn.epubee.com/files.aspx'
	# try:
	#	 req = requests.get(url, headers=header,proxies=proxy)
	#	 if req.status_code==200:
	#		 bsObj = BeautifulSoup(req.text, 'html.parser')
	#		 name_0 = bsObj.find('span', {'id': 'gvBooks_lblTitle_0'}).get_text()
	#		 format_0 = bsObj.find('a', {'id': 'gvBooks_gvBooks_child_0_hpdownload_0'}).get_text()
	#		 filename = name_0 + format_0
	#		 bid = bsObj.find('span', {'id': 'gvBooks_gvBooks_child_0_lblBID_0'}).get_text()
	#		 return filename, bid
	#	 else:
	#		 print('fail')
	#		 return
	# except:
	#	 print('fail')
	#	 return

	req = requests.get(url, headers=my_header, proxies=proxy)
	if req.status_code == 200:
#		print(u'add_book result : %s' % req.text)
		bsObj = BeautifulSoup(req.text, 'html.parser')
		try:
			allbooks = bsObj.find_all('p', class_='allbooks')[0].find_all('a')[1].get_text().strip()
			books_count = allbooks[allbooks.rfind('[') + 1:-1]
			for i in range(int(books_count)):
				name = bsObj.find('span', {'id': 'gvBooks_lblTitle_' + str(i)}).get_text()
				format = bsObj.find('a', {'id': 'gvBooks_gvBooks_child_' + str(i) + '_hpdownload_0'}).get_text()
				filename = name + format
				bid = bsObj.find('span', {'id': 'gvBooks_gvBooks_child_' + str(i) + '_lblBID_0'}).get_text()
				filesize = bsObj.find('span',{'id': 'gvBooks_gvBooks_child_' + str(i) + '_child_filesize_k_0'}).get_text()
				books.append({'filename': filename, 'bid': bid, 'filesize': filesize})
		except Exception as e :
			print(u'错误 %s' % e)
#			print('%s' % req.text)
	else:
		print('fail')
	return books

def gett_key(bid,proxy):
	url = u'http://cn.epubee.com/app_books/click_key.asmx/getkey'
	data = {'isVip': 1, 'uid': cookie.get('identify'),'strbid': bid}
	my_headers = {'Content-Type': 'application/json'}
	response = requests.post(url, headers=my_headers, json=data,proxies=proxy)
	dict = json.loads(response.content.decode())
	t_key=dict.get('d')[0]
	return t_key

def refreshpage(cookie, proxy):
	print(u'刷新页面中')
	cookie_str = cookie_toString(cookie)
#	uid = str(cookie.get('identify'))
#	t_key = gett_key(bid,proxy)
	url = u'http://cn.epubee.com/files.aspx'
	my_header = headers
	my_header['Cookie'] = cookie_str
	try:
		response = requests.get(url, headers=my_header, proxies=proxy)
	except Exception as e:
		print(u"刷新页面失败: %s" % e)
#	print(response.content)

def download(filename, bid, cookie,loc,proxy, size):
	retry_times = 1
	return_code = ''
	filename = loc + filename
	cookie_str = cookie_toString(cookie)
	uid = str(cookie.get('identify'))
	t_key = gett_key(bid,proxy)
	url = u'http://cn.epubee.com/getFile.ashx?bid=' + bid + u'&uid=' + uid + u'&t_key=' + t_key
	my_header = headers
	my_header['Cookie'] = cookie_str
	my_header['Referer' ] = 'http://cn.epubee.com/files.aspx'
	while retry_times > 0:
		retry_times -= 1
#		try:
		if 1 :
			response = requests.get(url, headers=my_header,proxies=proxy)
#		except Exception as e:
#			print(u'下载错误 (%s)' % e)
#		else:
			if response.status_code==200:
				down = response.content
				with open(filename, 'wb') as code:
					code.write(down)
#				if down.find("Ctrl+F5") :
#					print(u'%s' % down)
#					refreshpage(cookie, proxy)
#					time.sleep(3)
#					continue
				if size[-1:]=='K' :
					act_size=int(len(down)/1024)
					size=int(size[:-1])
					units = 'K'
				else :
					if size[-1:]=='M' :
						act_size=int(len(down)/1024/1024)
						size=int(size[:-1])
						units = 'M'
					else:
						act_size=len(down)
						size=int(size)
						units = ''
				if abs(float(act_size)/size -1) * 100 > 10 :       #下载文件与网页上显示的文件大小相差>10%,即下载出错或无法下载
					print(u'文件大小有误: 源%s%s<>实%s%s' % ( size , units, act_size , units))
					try:
						print(u'已下载内容: %s' % down[:100])
					except :
						print(u'未知错误')
					time.sleep(5)
					refreshpage(cookie, proxy)
					continue
				else:
					print(u'下载完成')
					return_code = bid
					break
			else:
				print(u'下载错误 (%s): %s' %(response.status_code, response.content))
	return return_code

def getSearchList(search_book_name, proxy):
	dict = []
	url='http://cn.epubee.com/keys/get_ebook_list_search.asmx/getSearchList'
	data={'skey':search_book_name}
	cookie_str = cookie_toString(cookie)
	my_header = headers
	my_header['Cookie'] = cookie_str
	try:
		response = requests.post(url,headers=my_header,json=data, proxies=proxy)
		if response.status_code == 200:
			dict = json.loads(response.content.decode())['d']
	except Exception as e:
		print(u'读取搜索出错%s' % e)
	print(u'搜索结果%s条' % len(dict))
#	print(dict)
	return dict

def get_book_id(dict_result, b_type):
	BID = []
	if len(dict_result)>0 :
		for i in range(0, len(dict_result)):
			if dict_result[i]['Title'].find("["+b_type+"]") > 0:
				BID.append((dict_result[i]['BID']))
	return BID

def delete_book(bids, cookie, proxy):
	cookie_str = cookie_toString(cookie)
	uid = str(cookie.get('identify'))
	if bids == "" :
		books = getBookList(cookie,proxy)
#		print(u'books list : %s' % (books))
		if len(books) >0 :
			bids = '0,'
			for book in books:
				bids += book.get("bid") + u','
			bids = bids[:-1]
#			print(u'bids : %s' % bids)
	data = {'uid': uid, 'bids': bids}
	url = u'http://cn.epubee.com/app_books/deletemybooks.asmx/deletemybooks'
	my_header = headers
	my_header['Cookie'] = cookie_str
	my_header['Referer'] = 'http://cn.epubee.com/files.aspx'
	try:
		response = requests.post(url, headers=my_header, json=data, proxies=proxy)
	except Exception as e:
		print(u'request : %s' % data)
		print(u'删除书本失败%s' % e)
	print(u"删除书本 %s, %s" %( response.status_code, response.content ))
	
def do_login(uuid,uupwd, cookie,proxy):
	print(u'登陆指定用户帐号: %s' % uuid)
	cookie_str = 'ASP.NET_SessionId='+str(cookie.get('ASP.NET_SessionId'))+'; leftshow=1'
	data = {'eID':uuid,'userpassword':uupwd}
	url="http://cn.epubee.com/keys/retrieve_cloud_id.asmx/Retrieve"
	my_header = headers
	my_header['Cookie'] = cookie_str
	my_header['Referer'] = 'http://cn.epubee.com/files.aspx'
#	try:
	if 1 :
		response = requests.post(url, headers=my_header, json=data,proxies=proxy)
		if response.status_code == 200:
			update_cookies(response.content.decode())
			print(u'登陆%s帐号成功' % uuid)
		else:
			print(u'登陆帐号失败：%s' % response.content)
#	except Exception as e:
#		print(u'登陆帐号失败%s' % e)
	return

def main():
	print time.strftime( "%Y%m%d-%H%M%S", time.localtime(time.time()))

#	loc=input("请输入存放地址：")
#	loc='F:\\资料\\电子书\\kindle\\'
	loc = '/root/down_book/'
#	下载地址---F:\资料\电子书\kindle\   KxrbnqbpG9yIpkxWSozxtw%3d%3d
#	book_name指定书名
#	book_name = "程序员的数学思维修炼（趣味解读）"
	book_name = ""
	book_type = ".mobi"
#	bs指定搜索结果前N项添加入书库
	bs = 3
#	mailto指定临时用户邮件发送
	mailto = 'aaaaabbbbb@kindle.cn'
#	eid,epwd指定用户email及密码(已经设置了Email或Name，不能用ID登录.)
	email="3333333333@163.com"      #设置切换登陆的用户名
	epwd=""                          #设置切换登陆的密

	path = '/root/down_book/ip.txt'  # 存放爬取ip的文档path，建议为全路径
	try: 
		with open(path, 'r+') as f:
			iplist = f.readlines()
		for i in range(0, len(iplist)):
			iplist[i] = iplist[i].strip('\n')
	except Exception as e:
		print(u'代理IP读取错误，跳过代理功能')
		iplist = [1]
		iplist[0] = ''
	try:
		while True:
			ip = random.choice(iplist)
			proxy={'http':ip,'https':ip}
			print(u'代理IP: %s' % proxy.get('http'))
			if getCookie(proxy) == 200:
				break
		print(u'当前uid是: %s' % cookie.get('identify'))
		if email <> "" :
			if 'uemail' in cookie :
				if str(cookie.get('uemail')) <> email :
					#重新登陆指定用户
					do_login( email, epwd, cookie, proxy )
			else:
				do_login(email, epwd, cookie, proxy)
		print(u'用户uid: %s' % str(cookie.get('identify')))
		time.sleep(1)
	except Exception as e:
		print("error %s" % e)
	else:
		if book_name <> "" :
#			获取图书测试
			search_result = getSearchList(book_name, proxy)
			#bookid = str(input(u'请输入：'))
			bookid = get_book_id(search_result, book_type)
			if len(bookid) > 0:

				for bb in range(3) :
					try:
						bid = bookid[bb]
						addbook = add_Book(cookie, bid,proxy)
						time.sleep(3)
					except :
						print(u'添加书库错误 (%s), %s' % (addbook,bid))
						break
		#取书库列表
		books_list = getBookList(cookie,proxy)
		done_list = ""
		if len(books_list) > 0 :
			print(u'书库数量: %s' % len(books_list) )
			for bl in range(len(books_list)):
				filename = books_list[bl]['filename']
				bid = books_list[bl]['bid']
				file_size =  books_list[bl]['filesize']
				print(u'开始下载 : %s, (%s), %s' % (filename, file_size, bid))
				if download(filename,bid,cookie,loc,proxy, file_size) <> '' :
					print(u'done! %s' % filename)
					done_list = done_list + str(bl) + " "
				else :
					print(u'下载失败 : %s' % filename)
		else :
			print(u'书库没有书')
		if len(done_list)>0 :
			print(u'通过邮件发送到: %s(Building....)' % cookie.get('uemail'))
			mailto = mailto + " " cookie.get('kindle_email')  + " " + cookie.get('uemail')
			mailto = mailto.strip().replace(" ",",").replace(",,", ",")
			for i in done_list.strip().split(' ') :
				send_mail(mailto, books_list[int(i)]['filename'], loc)
		if len(done_list)>0 :
			#删除下载成功的书
			delete_book("0," + done_list.strip().replace(' ',','), cookie , proxy)
	print(u'程序完成')
	
if __name__ == '__main__':
	main()
