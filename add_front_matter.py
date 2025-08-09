import os
import sys
import re

def add_front_matter(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and file not in {'tags.md', 'SUMMARY.md'}:
                file_path = os.path.join(root, file)
                add_front_matter_to_file(file_path)

def add_front_matter_to_file(file_path):
    file_name = os.path.basename(file_path)
    if file_name == 'README.md':
        tag = 'GITBOOK'
        category = 'GITBOOK'
    else:
        tag = os.path.basename(os.path.dirname(file_path))
        category = tag
    front_matter_tags = f"tags: {tag}\ncategories: {category}\n"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 檢查是否已經有 tags 和 categories
    has_tags = re.search(r'^tags: .*$', content, re.MULTILINE)
    has_categories = re.search(r'^categories: .*$', content, re.MULTILINE)

    # 如果不存在 tags 和 categories，則添加到文件末尾
    if not has_tags and not has_categories:
        # 添加到文件末尾
        updated_content = content.strip() + "\n\n---\n" + front_matter_tags + "\n---\n"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python add_front_matter.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    add_front_matter(directory)
