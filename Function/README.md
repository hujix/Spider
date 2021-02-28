# Function

总结功能：

此处所写为本人在自学爬虫过程中觉得比较实用的一些小功能！



#### m3u8 文件说明
**#EXTM3U**
>每个M3U文件第一行必须是这个tag，请标示作用

**#EXT-X-VERSION:3**
>该属性可以没有

**#EXT-X-MEDIA-SEQUENCE:140651513**
>每一个media URI在PlayList中只有唯一的序号，相邻之间序号+1,一个media URI并不是必须要包含的，如果没有，默认为0

**#EXT-X-TARGETDURATION**
>指定最大的媒体段时间长（秒）。所以#EXTINF中指定的时间长度必须小于或是等于这个最大值。这个tag在整个PlayList文件中只能出现一 次（在嵌套的情况下，一般有真正ts url的m3u8才会出现该tag）

**#EXT-X-PLAYLIST-TYPE**
>提供关于PlayList的可变性的信息，这个对整个PlayList文件有效，是可选的，格式
>如下：#EXT-X-PLAYLIST-TYPE:：如果是VOD，则服务器不能改变PlayList 文件；<br>
>如果是EVENT，则服务器不能改变或是删除PlayList文件中的任何部分，但是可以向该文件中增加新的一行内容。

**#EXTINF**
>duration指定每个媒体段(ts)的持续时间（秒），仅对其后面的URI有效，title是下载资源的url

**#EXT-X-KEY**
>表示怎么对media segments进行解码。其作用范围是下次该tag出现前的所有media URI，属性为NONE 或者 AES-128。NONE表示 URI以及IV（Initialization Vector）属性必须不存在， AES-128(Advanced EncryptionStandard)表示URI必须存在，IV可以不存在。

**#EXT-X-PROGRAM-DATE-TIME**
>将一个绝对时间或是日期和一个媒体段中的第一个sample相关联，只对下一个meida URI有效，
>格式如#EXT-X-PROGRAM-DATE-TIME:
>For example: #EXT-X-PROGRAM-DATETIME:2010-02-19T14:54:23.031+08:00

**#EXT-X-ALLOW-CACHE**
>是否允许做cache，这个可以在PlayList文件中任意地方出现，并且最多出现一次，作用效果是所有的媒体段。格式如下：#EXT-X-ALLOW-CACHE:

**#EXT-X-ENDLIST**
>表示PlayList的末尾了，它可以在PlayList中任意位置出现，但是只能出现一个。
>格式如下：#EXT-X-ENDLIST
