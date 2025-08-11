# -*- coding: utf-8 -*-

import argparse
import os
import re

# 需要略過整體掃描與 all.md 生成的資料夾
GLOBAL_IGNORES = ['_book', 'docs', 'images', 'node_modules', 'dict', '.git',
                  'image', 'scripts', 'styles']

# 不產生 all.md、也不在 SUMMARY 加 all.md 的資料夾
EXCLUDE_ALLMD_DIRS = set(['image', 'scripts', 'styles'])

README_DOT_MD = re.compile(r'^README\..+\.md$', re.IGNORECASE)

def output_markdown(dire, base_dir, output_file, append, iter_depth=0, chapter_counter=None):
    """
    遞迴列出所有目錄與檔案。
    - 不建立 0-README.md
    - 目錄主連結：README.md > 第一個 md 檔（排除 README.*.md）> 無連結
    - 產生 all.md（排除 EXCLUDE_ALLMD_DIRS）
    """
    # 初始化章節計數器
    if chapter_counter is None:
        chapter_counter = [0]
    
    for filename in sort_dir_file(os.listdir(dire), dire):
        if filename in GLOBAL_IGNORES:
            continue

        file_or_path = os.path.join(dire, filename)

        if os.path.isdir(file_or_path):
            if mdfile_in_dir(file_or_path):
                # 第一層目錄增加 Chapter 編號
                if iter_depth == 0:
                    chapter_counter[0] += 1
                    chapter_title = "Chapter {} {}".format(chapter_counter[0], filename)
                else:
                    chapter_title = filename
                
                # 目錄主連結目標
                index_md = choose_index_md(file_or_path)
                if index_md:
                    output_file.write(
                        '  ' * iter_depth +
                        '* [{}]({}/{})\n'.format(
                            chapter_title, rel_part(base_dir, file_or_path), index_md)
                    )
                else:
                    output_file.write('  ' * iter_depth + '* {}\n'.format(chapter_title))

                # 產生 all.md（除特定排除目錄）
                if filename not in EXCLUDE_ALLMD_DIRS:
                    create_all_md(file_or_path, base_dir)
                    output_file.write(
                        '  ' * (iter_depth + 1) +
                        '* [all]({}/{})\n'.format(
                            rel_part(base_dir, file_or_path), 'all.md')
                    )

                # 繼續遞迴
                output_markdown(file_or_path, base_dir, output_file, append, iter_depth + 1, chapter_counter)

        else:
            # 忽略 README.*.md
            if README_DOT_MD.match(filename or ''):
                continue

            md_title = is_markdown_file(filename)
            if md_title:
                if filename not in ['SUMMARY.md', 'SUMMARY-GitBook-auto-summary.md',
                                    'README.md', 'all.md']:
                    output_file.write(
                        '  ' * iter_depth + '* [{}]({})\n'.format(
                            write_md_filename(filename, append),
                            os.path.join(os.path.relpath(dire, base_dir), filename))
                    )

def choose_index_md(dire):
    """
    選目錄索引檔：
    1) all.md（優先）
    2) README.md（不分大小寫）
    3) 其餘 md 檔中的第一個（排除 SUMMARY* / all.md / README.*.md）
    4) 若無則回傳 None
    """
    entries = sorted(os.listdir(dire), key=str.lower)

    # 1) all.md 優先
    for name in entries:
        if name.lower() == 'all.md':
            return name

    # 2) README.md
    for name in entries:
        if name.lower() == 'readme.md':
            return name

    # 3) 第一個 md（排除不需要）
    for name in entries:
        if not is_markdown_file(name):
            continue
        if name in ['all.md'] or name.startswith('SUMMARY') or README_DOT_MD.match(name):
            continue
        return name

    return None

def mdfile_in_dir(dire):
    """該資料夾是否含有 .md/.markdown 檔"""
    for _, _, files in os.walk(dire):
        for filename in files:
            if README_DOT_MD.match(filename or ''):
                # 即便有 README.*.md，仍算有 md 檔讓目錄能被列入，但不會被選為索引
                return True
            if re.search(r'\.(md|markdown)$', filename, re.IGNORECASE):
                return True
    return False

def is_markdown_file(filename):
    """若是 Markdown 檔回傳去副檔名的檔名，否則回傳 False"""
    match = re.search(r'\.(md|markdown)$', filename, re.IGNORECASE)
    if not match:
        return False
    ext = match.group().lower()
    if ext == '.md':
        return filename[:-3]
    else:
        return filename[:-9]

def create_all_md(dire, base_dir, filename='all.md'):
    """
    為指定資料夾產生 all.md：
    - 僅列出該資料夾『同一層』的 Markdown 檔（不遞迴）
    - 排除 README.md、README.*.md、all.md、SUMMARY* 檔
    """
    lines = []
    rel_dir = os.path.relpath(dire, base_dir)
    title = os.path.basename(dire) or rel_dir
    lines.append(f'# {title} - 目錄索引\n\n')

    for fname in sorted(os.listdir(dire), key=str.lower):
        full = os.path.join(dire, fname)
        if os.path.isdir(full):
            continue
        if README_DOT_MD.match(fname or ''):
            continue
        md_title = is_markdown_file(fname)
        if not md_title:
            continue
        if fname in ['README.md', 'all.md'] or fname.startswith('SUMMARY'):
            continue
        # 與 all.md 同層 → 直接檔名
        lines.append(f'* [{md_title}]({fname})\n')

    with open(os.path.join(dire, filename), 'w', encoding='utf-8') as f:
        f.writelines(lines)

def sort_dir_file(listdir, dire):
    # 先檔案後目錄，再整體 a-z
    files, dirs = [], []
    for name in listdir:
        (dirs if os.path.isdir(os.path.join(dire, name)) else files).append(name)
    merged = files + dirs
    merged.sort(key=str.lower)
    return merged

def write_md_filename(filename, append):
    if append:
        for line in former_summary_list:
            if re.search(re.escape(filename), line):
                s = re.search(r'\[.*\]\(', line)
                return s.group()[1:-2]
        else:
            return is_markdown_file(filename)
    else:
        return is_markdown_file(filename)

def rel_part(base_dir, path):
    """取得 base_dir 到 path 的相對路徑（避免 Windows 反斜線）"""
    return os.path.relpath(path, base_dir).replace('\\', '/')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--overwrite', help='overwrite on SUMMARY.md', action="store_true")
    parser.add_argument('-a', '--append', help='append on SUMMARY.md', action="store_true")
    parser.add_argument('directory', help='the directory of your GitBook root')
    args = parser.parse_args()

    overwrite = args.overwrite
    append = args.append
    dir_input = args.directory

    if append and os.path.exists(os.path.join(dir_input, 'SUMMARY.md')):
        global former_summary_list
        with open(os.path.join(dir_input, 'SUMMARY.md'), encoding='utf-8') as f:
            former_summary_list = f.readlines()

    filename = 'SUMMARY.md' if (overwrite or not os.path.exists(os.path.join(dir_input, 'SUMMARY.md'))) \
               else 'SUMMARY-GitBook-auto-summary.md'

    with open(os.path.join(dir_input, filename), 'w', encoding='utf-8') as output:
        output.write('# Summary\n\n')
        # 顯示名稱改為 GITBOOK簡介
        output.write('* [GITBOOK簡介](./README.md)\n')
        output_markdown(dir_input, dir_input, output, append)

    return 0

if __name__ == '__main__':
    main()
