# -*- coding: utf-8 -*-
"""
@file：csv_helper.py
@description: csv文件处理
@author: longyunyue
@date：2021/8/9
"""

import codecs
import csv


def read_csv_rows(f_path):
	"""
	按照行来读取csv文件，返回一个结果列表
	:param f_path:
	:return:
	"""
	result = []
	f = open(f_path, 'r')
	with f:
		reader = csv.reader(f)
		for row in reader:
			for e in row:
				result.append(e)
	return result


def write_csv_rows(f_path, content_rows):
	"""
	将数据列表按行写入csv文件
	:param f_path:
	:param content_rows:
	:return:
	"""
	f = open(f_path, 'w')
	with f:
		writer = csv.writer(f)

		for row in content_rows:
			writer.writerow(row)


def read_csv_dict(f_path, post_process=None):
	"""
	读取字典形式csv数据
	:param post_process:
	:param f_path: 文件路径
	:return: 返回的行的类型是 OrderedDict
	"""
	import copy
	f = open(f_path, 'r')
	result = []
	with f:
		reader = csv.DictReader(remove_bom_from_line(line) for line in f)
		for row in reader:
			result.append(copy.deepcopy(row))
		if post_process:
			result = post_process(result)
		return result


def remove_bom_from_line(line):
	return line[3:] if line.startswith(codecs.BOM_UTF8) else line


def write_csv_dict(f_path, field_names, dict_rows, post_process=None):
	"""
	写csv字典文件
	:param post_process:
	:param f_path: 文件路径
	:param field_names: 表头
	:param dict_rows: 数据字典列表
	:return:
	"""
	import os
	cur_path = os.getcwd()
	folder = cur_path + '/LocalData/'
	if not os.path.exists(folder):
		os.makedirs(folder)
	f_path = folder + f_path
	f = codecs.open(f_path, 'wb')
	f.write(codecs.BOM_UTF8)
	with f:
		writer = csv.DictWriter(f, field_names, restval='null', extrasaction='ignore')
		writer.writeheader()
		# 导出后处理
		if post_process:
			dict_rows = post_process(dict_rows)
		writer.writerows(dict_rows)
		f.close()


def translate_excel_data(v):
	import ast
	if isinstance(v, long):
		v = int(v)
	if v in ('TRUE', 'True', 'true'):
		return True
	if v in ('FALSE', 'false', 'False'):
		return False
	try:
		v = v.replace('\n', '')
		v = ast.literal_eval(v)
	except:
		return v
	return v


def transfer_list_include_zh_to_str(data):
	"""
	将包含有中文的元素的列表数据转化成正确的utf-8字符串输出，中文元素用双引号包括
	:param data:
	:return:
	"""
	import json
	s = json.dumps(data, encoding="UTF-8", ensure_ascii=False)
	return s.encode('utf-8')

