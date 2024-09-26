"""
@File    :   utils.py
@Time    :   2024/09/26 10:40:58
@Author  :   TankNee
@Version :   1.0
@Desc    :   Utils
"""


import re


def markdown_table_to_json(markdown_table: str):
    """Convert a Markdown table to a list of dictionaries.

    Args:
        markdown_table (str): A Markdown table.

    Returns:
        list: A list of dictionaries.
    """
    lines = markdown_table.split("\n")
    headers = [
        header.strip() for header in re.split(r"\s*\|\s*", lines[0]) if header.strip()
    ]
    data_lines = [line for line in lines[2:] if line.strip()]
    json_list = []
    for line in data_lines:
        values = [
            value.strip() for value in re.split(r"\s*\|\s*", line) if value.strip()
        ]
        item = {}
        for i, header in enumerate(headers):
            item[header] = values[i]
        json_list.append(item)
    return json_list


def json_to_markdown_table(json_list: list):
    """Convert a list of dictionaries to a Markdown table.
    
    Args:
        json_list (list): A list of dictionaries.
    
    Returns:
        str: A Markdown table.
    """
    if not json_list:
        return ""
    # 获取表头（第一个字典的键）
    headers = list(json_list[0].keys())
    # 创建 Markdown 表格的表头行
    markdown_table = "| " + " | ".join(headers) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    # 添加数据行
    for item in json_list:
        values = [str(item[key]) for key in headers]
        markdown_table += "| " + " | ".join(values) + " |\n"
    return markdown_table
