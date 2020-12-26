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

## TScloud_dl

一键下载清华云盘共享文件  
清华云盘共享文件在浏览器中仅支持单文件下载（虽然有下载文件夹的选项，但往往因大小超出限制而无法下载），本程序允许用户直接下载全部文件（未压缩），支持多重文件夹。

说明：
`main(share_id: str, pwd: str = None, folder: Optional[list] = None, file: bool = True)`各参数用法：

* `share_id`：共享链接的`id`，形如`f7aa551c8d3a4540a091`（注：这是一个无效`id`，仅作示例用）
* `pwd`：下载密码，如果不需要密码，本参数无用，如果需要密码，会优先使用本密码，无效则要求输入
* `folder`：要下载的文件夹（仅限根目录中，子目录文件夹一律下载），不传参时，默认下载全部文件夹，传入`['']`不下载文件夹，传入`['folder_01', 'folder_02', ...]`下载列表中的文件夹
* `file`：是否下载单文件（仅限根目录中，子目录单文件一律下载），不传参时，默认下载

## media_converter

将多媒体文件（包括但不限于`flv/wav/mp3`）转换为给定比特率的`mp3`（也可以是别的）

之前一直用`Emisoft Media Converter`把从b站扒下来的pv转成音频拷到随身听里，结果今天那玩意突然用不了了......就整了这么个东西，ffmpeg yyds!

## change_encoding

批量改编码格式

鼓捣`windows`的时候开启了个什么`utf-8`支持（还是`beta`版的），结果整的我电脑上文本文件编码全乱了qwq
