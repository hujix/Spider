# Python-Spider

## 介绍：

此处收录本人从**自学**爬虫开始所写的所有案例！

部分代码的解释，我都写成了博客放在了我的 [CSDN主页](https://blog.csdn.net/qq_44700693) 上。

## 文件注释

| 文件名             | 文件说明                                                                                                                                                                                                                                                                                |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BaiduTranslate  | 百度翻译接口（V2）破解，内含扣出的js代码                                                                                                                                                                                                                                                              |
| AcFun.py        | 一个类似于B站的动漫网站：[【AcFun主页】](https://www.acfun.cn/) <br>无需会员直接下载最高清晰度。<br> CSDN博文地址：[Python爬虫：AcFun弹幕视频网](https://blog.csdn.net/qq_44700693/article/details/109124334)                                                                                                                  |
| AGE-requests.py | 利用 **requests** 爬取该网站，也是一个动漫网站（不过好像叫AGE动漫的网站有好几个~）：[【AGE动漫】](https://agefans.org/) <br> CSDN博文地址： [Python爬虫：AGE动漫下载之 requests 版](https://blog.csdn.net/qq_44700693/article/details/107510787)                                                                                       |
| AGE-selenium.py | 利用 **selenium** 爬取该网站，和 **requests** 版的网站一样：[【AGE动漫】](https://agefans.org/) <br> CSDN博文地址：[Python爬虫：AGE动漫下载之 selenium 版](https://blog.csdn.net/qq_44700693/article/details/107877836)                                                                                               |
| BiAn.py         | 一个壁纸网站：[【彼岸图网】](https://pic.netbian.com/) <br> 爬取的是每个图片详情页的概览图，**并不是原图**，虽然我尝试这找到了原图的请求方式，但是接口内部会进行身份验证，目前的我没有什么办法。                                                                                                                                                                 |
| BiLiBiLi.py     | B站，这个就不用太多说了吧：[【哔哩哔哩动画】](https://www.bilibili.com/) <br> 有大会员可以下载 **4K** 视频。<br>CSDN博文主页：[Python爬虫：哔哩哔哩（bilibili）视频下载](https://blog.csdn.net/qq_44700693/article/details/108828909)                                                                                                 |
| DSP.py          | 各大短视频平台无水印解析。<br> 目前已支持的平台：皮皮虾（已更新最新版解析方式）、皮皮搞笑、抖音、抖音火山版、抖音极速版、腾讯微视、开眼视频、快手、快手极速版、最右、VUE、看看视频、西瓜视频...（目前仍在更新中...）<br> CSDN博文地址：[Python爬虫：短视频平台无水印下载（上）](https://blog.csdn.net/qq_44700693/article/details/108089085)                                                                | 
| DuiTang.py      | 一个有好看的图片的网站：[【堆糖】](https://www.duitang.com/) <br> 直接从搜索的接口开始解析的。                                                                                                                                                                                                                    |
| Emoji.py        | 一个有大量表情包的网站：[【发表情】](https://www.fabiaoqing.com/) <br> 提供三种选择方式：1.热门表情 2.获取菜单 3.搜索下载                                                                                                                                                                                                 |
| Emoji-GUI.py    | 利用 **tkinter** 编写的表情包界面版。<br> **该项目写了一大半了，还未收尾~**                                                                                                                                                                                                                                   |
| GuShiWen.py     | [古诗文网](https://www.gushiwen.cn/) 登录验证码破解                                                                                                                                                                                                                                            |
| Haokan.py       | 一个短视频网站：[【好看视频】](https://haokan.baidu.com/)                                                                                                                                                                                                                                         |
| IP-Post.py      | 一个提供免费 **代理IP** 的网站：[【快代理】](https://www.kuaidaili.com/free/) <br>其实可以更改为数据库版的，用的时候方便点。<br> CSDN博文地址：[Python爬虫：自建IP地址池](https://blog.csdn.net/qq_44700693/article/details/105846658)                                                                                                 |
| JiJianBZ.py     | 一个 **非常良心** 的壁纸网站，壁纸原图不限量下载：[【极简壁纸】](https://bz.zzzmh.cn/) <br> 这个项目涉及到了一点点 **JS逆向**。                                                                                                                                                                                               |
| Mzitu.py        | 用 **BeautifulSoup4** 来解析。嘿嘿嘿，**dddd** (懂得都懂)~ [【妹子图】](https://www.mzitu.com/) <br> CSDN博文地址：[Python爬虫：爬取网页图片](https://blog.csdn.net/qq_44700693/article/details/105598212)                                                                                                          |
| Mzitu-XPath.py  | 用 **XPath** 来解析。网站还是上边那个：[【妹子图】](https://www.mzitu.com/)                                                                                                                                                                                                                            |
| OKzyw.py        | 一个视频资源网站：[【OK资源网】](http://www.okzyw.net/) <br> 该项目中使用到了第三方工具：**ffmpy3**。                                                                                                                                                                                                            |
| PianKu.py       | 一个在线视频网站：[【片库】](https://www.mypianku.com/) <br> 片库的地址变了：原来是：[https://www.pianku.tv](https://www.pianku.tv)，现在是：[https://www.mypianku.com/](https://www.mypianku.com/) <br> CSDN博文地址：[Python爬虫：爬取链接被加密的网站中的视频《传闻中的陈芊芊》](https://blog.csdn.net/qq_44700693/article/details/106389711) |
| ts-Download.py  | 借助[【片库】](https://www.mypianku.com/) 网站的视频来简单说说我的小想法。 <br> CSDN博文地址：[Python爬虫：用最普通的方法爬取ts文件并合成为mp4格式](https://blog.csdn.net/qq_44700693/article/details/106189511)                                                                                                                   |
| WordCloud.py    | 两个画词云的项目：<br> 1、疫情词云 --- 借助第三方接口获取疫情数据。 <br> 2、流行词词云 --- 通过[【小鸡词典】](https://jikipedia.com/) 获取流行词数据。                                                                                                                                                                                |
| ZzzFun.py       | 一个动漫视频网站：[【ZzzFun动漫视频网】](http://www.zzzfun.com/) <br> 该网站特性：按下 **F12** 后会跳转回首页。<br> CSDN博文地址：[Python爬虫：ZzzFun动漫视频网](https://blog.csdn.net/qq_44700693/article/details/109924262)                                                                                                    |


