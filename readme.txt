这是一个模拟在epubee网站上下载电子书的代码（这是一个Fork过来的项目基础上修改的）
其中参考了另一个项目：https://github.com/Hxiaodou/kindleTool/blob/master/kindletool/epubee.py

ip.txt是IP代理地址，可以从另一个github项目中扫描得到https://github.com/hohohoesmad/PrxGetter

运行时需要修改epubee_book.py里面几个地方：
1、book_name： 书名，匹配得越准确越好，程序会自动从epubee搜索并添加可能的结果（前3个，因为免费用户限每日添加3本书，所以书名越准确结果越匹配），如果不需要自动搜索添加（配合下面第3点的切换用户，可实现先手工搜索并添加书名再定时下载），则book_name=""   
    
2、loc书下载后目录，最好为全路径   
   
3、email和epwd为指定切换用户的邮箱和密码，用于方便通过网站页面手工添加书后，再用程序下载，email留空则为不切换
