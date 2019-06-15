这是一个模拟在epubee网站上下载电子书的代码（这是一个Fork过来的项目基础上修改的）
其中参考了另一个项目：https://github.com/Hxiaodou/kindleTool/blob/master/kindletool/epubee.py

ip.txt是IP代理地址，可以从另一个github项目中扫描得到PrxGetter

运行时需要修改epubee_book.py里面两个地方：
book_name书名，匹配得越准确越好，程序会自动从epubee搜索并添加可能的结果（前3个，因为免费用户限每日添加3本书，所以书面越准确结果越匹配）
loc书下载后目录