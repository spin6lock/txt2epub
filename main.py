import argparse
import os
import re
import subprocess
import time

def process_txt(input_file, output_file, author, title):
    # 定义章节和卷的正则表达式
    chapter_pattern = re.compile(r'^\s*[第][0123456789ⅠI一二三四五六七八九十零序〇百千两][章].*')
    volume_pattern = re.compile(r'^\s*[第][0123456789ⅠI一二三四五六七八九十零序〇百千两][卷].*')
    volume_pattern2 = re.compile(r'^\s*[卷][0123456789ⅠI一二三四五六七八九十零序〇百千两].*')
    intro_pattern = re.compile(r'^\s*(楔子|序章|序言|序|引子).*')

    # 读取输入文件并处理
    read_start = time.perf_counter()
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    read_end = time.perf_counter()

    # 写入临时文件
    add_section_start = read_end
    temp_txt_file = 'temp_processed.txt'
    new_content = []
    for line in content.splitlines():
        # 找到并标记所有章节和卷
        if chapter_pattern.match(line) or intro_pattern.match(line):
            new_line = "## " + line
            new_content.append(new_line)
        elif volume_pattern.match(line) or volume_pattern2.match(line):
            new_line = "# " + line
            new_content.append(new_line)
        else:
            new_content.append(line)
    add_section_end = time.perf_counter()

    write_start = add_section_end
    with open(temp_txt_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_content))
    write_end = time.perf_counter()

    # 使用 pandoc 转换为 epub
    print("处理完毕，开始调用pandoc")
    pandoc_start = write_end
    pandoc_command = [
        'pandoc', temp_txt_file, '-o', output_file,
        '--epub-chapter-level=2',
        '--metadata', f'author={author}',
        '--metadata', f'title={title}'
    ]
    subprocess.run(pandoc_command)
    pandoc_end = time.perf_counter()

    # 删除临时文件
    os.remove(temp_txt_file)
    print(f"读取耗时：{read_end-read_start:.2f} 处理耗时:{add_section_end-add_section_start:.2f} \
写入耗时：{write_end-write_start:.2f} pandoc耗时:{pandoc_end-pandoc_start:.2f}")

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Convert a txt file to epub format.')
    parser.add_argument('input_file', help='Input text file')
    parser.add_argument('output_file', help='Output epub file')
    parser.add_argument('author', help='Author of the work')
    parser.add_argument('title', help='Title of the work')

    args = parser.parse_args()

    # 调用处理函数
    process_txt(args.input_file, args.output_file, args.author, args.title)

if __name__ == '__main__':
    main()

