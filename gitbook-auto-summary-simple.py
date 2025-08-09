import os

def generate_summary(directory):
    summary_path = os.path.join(directory, 'SUMMARY.md')
    with open(summary_path, 'w', encoding='utf-8-sig') as f:
        f.write('#\n\n')
        f.write('\n### GITBOOK架設說明\n\n')
        f.write('* [{}]({})\n'.format("GITBOOK簡介", "README.md"))
        f.write('\n#\n')
        
        # Check if there is a "0-README.md"
        has_readme_intro = any(item.lower() == '0-readme.md' for item in os.listdir(directory))
       # print(has_readme_intro)
        generate_summary_recursive(directory, f, level=1, indent=4)
        f.write('\n### 標籤彙整頁\n\n')  # 新增標籤彙整頁的標題
        f.write('* [{}]({})\n'.format("tags", "tags.md"))  # 新增標籤彙整頁的條目

def generate_summary_recursive(directory, f, level, indent):
    for item in sorted(os.listdir(directory)):
        if item.startswith('.'):
            continue  # Skip hidden files and directories
        full_path = os.path.join(directory, item)
        if os.path.isdir(full_path):
            header = item.replace('-', '*')  # Replace '-' with '*'
            if header in ["styles", "_book", "node_modules", "scripts"]:
                continue
            if indent:
                f.write('\n{} {}\n\n'.format('#' * (level + 1), header))
            else:
                f.write('\n{} {}\n\n'.format('#' * level, header))
            generate_summary_recursive(full_path, f, level + 1, indent)
        elif item in ["SUMMARY.md", "CHANGELOG.md","tags.md"]:
            continue
        elif item.endswith('.md'):
            header = directory.replace(".\\", "")
            if item.lower() == '0-readme.md':
                f.write('* [{}]({})\n'.format(header + "學習資源簡介", header + "/" + item))
            else:
                if indent:
                    f.write('  * [{}]({})\n'.format(item[:-3], header + "\\" + item))
                else:
                    f.write('* [{}]({})\n'.format(item[:-3], header + "\\" + item))

if __name__ == '__main__':
    book_directory = '.'
    generate_summary(book_directory)
    print('Summary.md and tags.md files generated successfully.')