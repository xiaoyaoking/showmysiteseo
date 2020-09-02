# showmysiteseo
show my site seo info

展示批量网站SEO信息的小工具

web 目录随便丢到一个站点里。
code 目录随便丢到个目录下 修改配置文件

比如 web 目录在 /home/wwwroot/www.test.com/xxx/
配置文件中要修改 jsonpath 为 /home/wwwroot/www.test.com/xxx/

后台服务部分：
python 需要安装 requests
命令：pip install requests

运行程序：
命令：nohup python xysite.py >/dev/null 2>&1 &


配置文件：xysite.json

{

    "time":120,  // 数据抓取时间
    
    "jsonpath":"web/",  //数据保存目录 
    
    "sitelist":["baidu.com","qq.com","wanren.com"] //网站域名列表 
    
}
