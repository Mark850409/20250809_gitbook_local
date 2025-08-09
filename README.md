# 架設GITBOOK


## 簡介

學習如何透過`docker`架設`GITBOOK`



## 目錄
- [架設GITBOOK](#架設gitbook)
  - [簡介](#簡介)
  - [目錄](#目錄)
  - [專案架構](#專案架構)
  - [一、事前準備](#一事前準備)
  - [二、安裝步驟(以windows本地建立為主)](#二安裝步驟以windows本地建立為主)
  - [三、成功畫面](#三成功畫面)


## 專案架構
```
GItbook(local)
├─ book.json
├─ gitbook-auto-summary.py
├─ package.json
├─ README.md
├─ styles
│  └─ website.css
├─ SUMMARY.md
```

## 一、事前準備

1. 請先確定`windows`有安裝`nodejs&&npm`

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_85c09b180f9136ea0c7843bbd8fc2b1a.png)


> [!note] 小提示
>1. 請注意，nodejs請安裝舊版本，否則會出現錯誤!!!
>2. 實測之後建議安裝node js V12.22.12版本，太高的版本也會出現錯誤!!!
>3. README.md && SUMMARY.md檔案必須存在，否則會出現錯誤!!!)

輸入以下指令安裝gitbook

```javascript
npm install -g gitbook-cli
```

看到此畫面表示安裝成功

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407211523142.png)




> [!note] 小提示
>1. gitbook-auto-summary.py 自動化目錄產生批次檔
>2. book.json gitbook部署設定檔
>3. website.css  gitbook樣式設定檔
>4. README.md 筆記檔
>5. SUMMARY.md 目錄檔


1. 請先撰寫`gitbook-auto-summary.py`

```python
# -*- coding: utf-8 -*-

import argparse
import os
import re


def output_markdown(dire, base_dir, output_file, append, iter_depth=0):
    """Main iterator for get information from every file/folder

    i: directory, base directory(to calulate relative path), 
       output file name, iter depth.
    p: Judge is directory or is file, then process .md/.markdown files.
    o: write .md information (with identation) to output_file.
    """
    ignores = ['_book', 'docs', 'images', 'node_modules', 'dict', '.git']

    for filename in sort_dir_file(os.listdir(dire), base_dir):
        # add list and sort
        if filename in ignores:
            print('continue ', filename)  # output log
            continue

        print('Processing ', filename)  # output log
        file_or_path = os.path.join(dire, filename)
        if os.path.isdir(file_or_path):  #is dir
            if mdfile_in_dir(file_or_path):
                # if there is .md files in the folder, output folder name
                # output_file.write('  ' * iter_depth + '* ' + filename + '\n')
                createRead0(file_or_path, '0-README.md')
                output_file.write('  ' * iter_depth + '* [{}]({}/{})\n'.format(
                    filename, filename, '0-README.md'))
                output_markdown(file_or_path, base_dir, output_file, append,
                                iter_depth + 1)  # iteration
        else:  # is file
            if is_markdown_file(filename):
                # re to find target markdown files, $ for matching end of filename
                if (filename not in [
                        'SUMMARY.md', 'SUMMARY-GitBook-auto-summary.md',
                        '0-README.md', 'README.md'
                ]):
                    #or iter_depth != 0): # escape SUMMARY.md at base directory
                    output_file.write(
                        '  ' * iter_depth + '* [{}]({})\n'.format(
                            write_md_filename(filename, append),
                            os.path.join(
                                os.path.relpath(dire, base_dir), filename)))
                    # iter depth for indent, relpath and join to write link.


def mdfile_in_dir(dire):
    """判断目录中是否有MD文件

    """
    for root, dirs, files in os.walk(dire):
        for filename in files:
            if re.search('.md$|.markdown$', filename):
                return True
    return False


def is_markdown_file(filename):
    """ 判断文件名是.Markdown

    i: filename
    o: filename without '.md' or '.markdown'
    """
    match = re.search('.md$|.markdown$', filename)
    if not match:
        return False
    elif len(match.group()) is len('.md'):
        return filename[:-3]
    elif len(match.group()) is len('.markdown'):
        return filename[:-9]


#create 0-README.md
def createRead0(dir_input, filename):
    readmeFile = open(os.path.join(dir_input, filename), 'w')
    readmeFile.close()
    print('createRead0 ', filename)  # output log


def sort_dir_file(listdir, dire):
    # sort dirs and files, first files a-z, then dirs a-z
    list_of_file = []
    list_of_dir = []
    for filename in listdir:
        if os.path.isdir(os.path.join(dire, filename)):
            list_of_dir.append(filename)
        else:
            list_of_file.append(filename)
    for dire in list_of_dir:
        list_of_file.append(dire)
    list_of_file.sort(key=str.lower)
    return list_of_file


def write_md_filename(filename, append):
    """ write markdown filename

    i: filename and append
    p: if append: find former list name and return
       else: write filename
    """
    if append:
        for line in former_summary_list:
            if re.search(filename, line):
                s = re.search('\[.*\]\(', line)
                return s.group()[1:-2]
        else:
            return is_markdown_file(filename)
    else:
        return is_markdown_file(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o',
        '--overwrite',
        help='overwrite on SUMMARY.md',
        action="store_true")
    parser.add_argument(
        '-a', '--append', help='append on SUMMARY.md', action="store_true")
    parser.add_argument('directory', help='the directory of your GitBook root')
    args = parser.parse_args()
    overwrite = args.overwrite
    append = args.append
    dir_input = args.directory

    # print information
    print('GitBook auto summary:', dir_input)
    if overwrite:
        print('--overwrite')
    if append and os.path.exists(os.path.join(dir_input, 'SUMMARY.md')):
        #append: read former SUMMARY.md
        print('--append')
        global former_summary_list
        with open(os.path.join(dir_input, 'SUMMARY.md')) as f:
            former_summary_list = f.readlines()
            f.close()
    print()
    # output to flie
    if (overwrite == False
            and os.path.exists(os.path.join(dir_input, 'SUMMARY.md'))):
        # overwrite logic
        filename = 'SUMMARY-GitBook-auto-summary.md'
    else:
        filename = 'SUMMARY.md'
    output = open(os.path.join(dir_input, filename), 'w')
    output.write('# Summary\n\n')
    output.write('* [README](./README.md)\n')
    output_markdown(dir_input, dir_input, output, append)
    output.close()
    print('GitBook auto summary finished:) ')
    return 0


if __name__ == '__main__':
    main()

```

2. 撰寫`book.json`

```json
{
    "title": "mark個人技術文章",
    "author": "mark",
    "description": "knowhow來自於個人經驗的累積",
    "theme-default":
    {
        "showLevel": true
    },
    "links":{
        "sidebar":{
            "自動化CICD-Jenkins":"https://markweb.idv.tw:46443",
            "程式碼倉庫-Gitlab":"https://markweb.idv.tw:10443",
            "Docker私有倉庫":"https://markweb.idv.tw:29443",
            "hexo部落格":"https://markweb.idv.tw:23443"
        }
    },
    "language" : "zh-hans",
    "plugins":
    [
        "-fontsettings",
        "cuav-chapters",
        "heading-anchors",
        "splitter",
        "hide-element",
        "expandable-chapters-small",
        "sidebar-style",
        "code",
        "-lunr", 
        "-search",
        "search-plus",
        "-sharing",
        "sharing-plus",
        "-highlight",
        "pageview-count",
        "chapter-fold",
        "tbfed-pagefooter",
        "github",
        "flexible-alerts",
        "prism",
        "back-to-top-button",
        "auto-scroll-table",
        "popup",
        "insert-logo",
        "edit-link",
        "chart",
        "page-treeview",
        "codeblock-filename",
        "klipse",
        "theme-comscore",
        "theme-mytest"
    ],
    "variables":
    {
        "mytest":
        {
            "nav":
            [
                {
                    "url": "https://markweb.idv.tw:10443/",
                    "target": "_blank",
                    "name": "我的Gitlab"
                },
                {
                    "url": "https://markweb.idv.tw:46443",
                    "target": "_blank",
                    "name": "我的Jenkins"
                },
                {
                    "url": "https://markweb.idv.tw:23443",
                    "target": "_blank",
                    "name": "我的hexo"
                },
                {
                    "url": "https://markweb.idv.tw:29443",
                    "target": "_blank",
                    "name": "我的Docker倉庫"
                }
            ]
        }
    },
    "style": {
        "website": "styles/website.css"
    },
    "pdf":{
        "pageNumbers":true,
        "fontFamily":"Arial",
        "fontSize":12,
        "paperSize":"a4",
        "margin":{
            "right":62,
            "left":62,
            "top":56,
            "bottom":56
        }
    },
    "pluginsConfig":
    {
        "sidebar-style": {
            "title": "《markhsu的筆記》",
            "author": "markhsu"
        },
        "hide-element":
        {
            "elements":
            [
                ".gitbook-link",
                ".title",
                ".treeview__copyright",
                ".treeview__main-title"
            ]
        },
        "edit-link": {
                "base": "https://markweb.idv.tw:10443/gitbooknpmproject/gitlabpageforgitbook/-/tree/master/",
                "label": "編輯此頁面"
         },
        "customtheme":
        {
            "search-placeholder": "請輸入關鍵字進行搜尋",
            "logo": "/README.assets/logo.svg",
            "favicon": "/README.assets/favicon.ico"
        },
        "tbfed-pagefooter":
        {
            "copyright": "Copyright &copy markweb 2024",
            "modify_label": "文章更新時間：",
            "modify_format": "YYYY-MM-DD HH:mm:ss"
        },
        "github":
        {
            "url": "https://github.com/Mark850409?tab=repositories"
        },
        "flexible-alerts":
        {
            "style": "callout",
            "comment":
            {
                "label": "Comment",
                "icon": "fa fa-comments",
                "className": "info"
            }
        },
        "sharing": {
            "douban": false,
            "facebook": true,
            "google": true,
            "hatenaBookmark": false,
            "instapaper": false,
            "line": true,
            "linkedin": false,
            "messenger": false,
            "pocket": false,
            "qq": false,
            "qzone": false,
            "stumbleupon": false,
            "twitter": true,
            "viber": false,
            "vk": false,
            "weibo": true,
            "whatsapp": true,
            "all": [
                "facebook", "google", "twitter",
                "line", "whatsapp"
            ]
        },
        "insert-logo": {
            "url": "https://markweb.idv.tw:10443/gitbooknpmproject/gitlabpageforgitbook/-/raw/master/logo.png?ref_type=heads",
            "style": "background: none; max-height: 60px; min-height: 60px"
        },
        "prism":
        {
            "css":
            [
                "prismjs/themes/prism-tomorrow.css"
            ],
            "lang":
            {
                "flow": "typescript"
            },
            "ignore":
            [
                "mermaid",
                "eval-js",
                "ascii",
                "result",
                "manifest",
                "payload",
                "google",
                "tree",
                "java_out",
                "log4j2",
                "jsp",
                "class",
                "Exception",
                "stack",
                "c#",
                "xml-dtd",
                "C++",
                "twig",
                "jinja2",
                "exception",
                "tpl"
            ]
        }
    }
}

```

3. 撰寫客製化CSS，請建立`styles/website.css`

```css
.markdown-section p{
  margin-top: revert;
}
.note.default {
  background-color: transparent;
  border: 1px solid #777;
  border-left-color: #777;
  border-left: 5px solid #777;
  border-radius: 3px;
  color: #777;
  padding: 10px 12px;
}
.note.primary {
  background-color: transparent;
  border: 1px solid #9779cf;
  border-left-color: #6f42c1;
  border-left: 5px solid #9779cf;
  border-radius: 3px;
  color: #6f42c1;
  padding: 10px 12px;
}
.note.info {
  background-color: transparent;
  border: 1px solid #428bca;
  border-left: 5px solid #428bca;
  border-radius: 3px;
  color: #428bca;
  padding: 10px 12px;
}
.note.success {
  color: #5cb85c;
  background-color: transparent;
  border: 1px solid #5cb85c;
  border-left: 5px solid #5cb85c;
  border-radius: 3px;
  padding: 10px 12px;
}
.note.warning {
  background-color: #fdf8ea;
  background-color: transparent;
  border: 1px solid #f0ad4e;
  border-left: 5px solid #f0ad4e;
  color: #f0ad4e;
  border-radius: 3px;
  padding: 10px 12px;
}
.note.danger {
  color: #d9534f;
  background-color: transparent;
  border: 1px solid #d9534f;
  border-left: 5px solid #d9534f;
  border-radius: 3px;
  padding: 10px 12px;
}
```
4. 產生`README.md` && `SUMMARY.md` 兩個檔案

* README.md要自己`手動建立`
* SUMMARY.md可以透過`程式建立`

```python
python gitbook-auto-summary.py -o .
```

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_841961cccd8efca71e75c408119c0da4.png)

5. 如果產生目錄檔案後發現檔案編碼不是`UTF-8`，記得要用`NOTEPAD++`改一下

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_ee8e50af40d6cdb0d248ec7a933928c9.png)

6. 輸入以下指令，初始化gitbook
```bash
gitbook init
```
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_4761bcb86e20c8bce710357b81bd26e7.png)

7. 輸入以下指令，安裝gitbook套件
```bash
gitbook install
```
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_039a470ebb62a9165bfe68ca31759531.png)

8. 輸入以下指令，打包gitbook
```bash
gitbook build
```
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_fd926e44323fcaef7c79c65941361556.png)

9. 輸入以下指令，部署gitbook
```bash
gitbook serve
```
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_032b5d19c39ea3c5d08b18d3bfc2d63c.png)


> [!note] 小提示
>這問題目前是個bug，官方尚未提出解決方案，請依照上面路徑，將62~64行註解掉即可。

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407211533408.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407211542480.png)


## 三、成功畫面
看到如下圖畫面表示成功

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_4d680e8d915f94c256ce077b72c93d90.png)

---
tags: GITBOOK
categories: GITBOOK

---
