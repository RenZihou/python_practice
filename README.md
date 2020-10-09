# python_practice

一些小的 Python 项目

## WeChat_img_decrypt

微信电脑版在储存聊天中的图片时采用异或运算进行了简单加密，本文件用于解密  
加密所用到的16进制数因客户端而异

## wlan_pwd

获取PC上储存的无线网络密码，储存到指定的`csv`文件中  
该程序会申请管理员权限以得到密码（[相关文档](https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecutea)）  
*仅适用于中文版 Windows*

## merge_flv

从b站上下载的番剧很多都是分段的，这样就没有办法在本地完整加载弹幕池  
此程序用于合并这些分段视频  
**请放到同一个目录下执行，且这个目录中最好不要有其它文件，否则可能造成其文件名被修改**  
视频分组是根据弹幕文件（`.ass`）进行分组的，因此请确保下载了弹幕文件并放置于同一目录下  
*需要安装`ffmpeg`并配置`PATH`*（无需安装相应的包）

合并视频：`ffmpeg -f concat -i parts.txt -c copy out.flv`  
转换格式：`ffmpeg -i in.flv -c copy -copyts out.mp4`

## bigjpg

调用 [Bigjpg](https://bigjpg.com/) 的`api`对图片进行放大  
参数在源码里有说明，相应的官方文档中也有（需登录），就不抄了  
对于本地图片和p站上的图片（图床域名`i.pximg.net`），需要先将图片托管到 [sm.ms](https://sm.ms/) 上，这个图床也提供了 [api](https://doc.sm.ms/)

## truth_table

打印给定的合式公式的真值表

说明：  
用大写英文字母`A-Z`表示命题变项  
用`~, &, |, ^, >, =`分别表示非、与、或、亦或、蕴涵、双蕴含  
用`()`表示括号  
空格不会影响判定

~作业出来四个小时就有卷王提交`CPP`版本了，然而`Python`yyds，一行`eval()`解决一切问题（bushi）~
