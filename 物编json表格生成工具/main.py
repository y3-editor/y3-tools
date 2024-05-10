# -*- coding: utf-8 -*-
import copy
import os
import shutil
import sys
import json



filedir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.realpath(os.path.join(filedir, "src", "Lib")))
sys.path.append(os.path.realpath(os.path.join(filedir, "src", "utils")))

from src.utils.json_helper import _JsonObjHook, hint_tuples
from src.utils.excel_helper import read_csv_dict_from_excel
import csv_helper
from hash_helper import hash_func


def read_config():
	config_file = os.path.join(os.path.dirname(__file__), 'config.json')
	config = json.load(open(config_file))
	return config


def read_template_json_by_table(table_name):
	template_file = os.path.join(os.path.dirname(__file__), 'template/' + table_name + '.json')
	f = open(template_file, 'r')
	json_data = json.load(f, encoding="utf-8")
	temp_data = _JsonObjHook(json_data)
	return temp_data


def gen_one(MAP_DIR, table_name, one_conf, zh_lan_data, en_lan_data):
	localize_keys = ('name', 'desc')
	hash_prefix_map = {
		'editor_unit': 'unit',
		'editor_decoration': 'decoration',
		'editor_item': 'item',
		'projectile_all': 'projectile',
		'ability_all': 'ability',
		'technology_all': 'technology',
		'editor_destructible': 'destructible',
		'sound_all': 'sound',
		'modifier_all': 'modifier',
	}
	key = one_conf.get('key')
	sub_dir = table_name.replace('_', '')
	file_path = os.path.join(MAP_DIR, 'editor_table', sub_dir, str(key) + '.json')
	ret = {}
	if os.path.exists(file_path):
		ret = _JsonObjHook(json.load(open(file_path, 'r'), encoding="utf-8"))
	# 处理多语言
	for k in localize_keys:
		if k in one_conf:
			hash_format = hash_prefix_map.get(table_name, table_name) + '_{}_' + str(k)
			hash_key = hash_format.format(key)
			tid = hash_func(hash_key)
			zh_lan_data[tid] = one_conf[k]
			en_lan_data[tid] = one_conf[k]
			one_conf[k] = tid
	ret.update(hint_tuples(one_conf))
	json_data = json.dumps(ret, ensure_ascii=True, indent=4, encoding="utf-8")
	with open(file_path, 'w') as writter:
		writter.write(json_data)
	print 'Gen Json Data: '+ '[' + table_name + ']' + str(key) + '.json'


def gen_file_by_table(MAP_DIR, table_name, zh_lan_data, en_lan_data):
	template = read_template_json_by_table(table_name)
	def_excel = os.path.join(os.path.dirname(__file__), 'excel/' + table_name + '.xlsx')
	excel_data = read_csv_dict_from_excel(def_excel)
	sheet_data = excel_data.get('def')
	for item in sheet_data[1:]:
		one_conf = copy.deepcopy(template)
		ret = {}
		for k,v in item.iteritems():
			ret[k] = csv_helper.translate_excel_data(v)
		one_conf.update(ret)
		gen_one(MAP_DIR, table_name, one_conf, zh_lan_data, en_lan_data)


def main(argv):
	# 检查命令行参数的数量
	print 'argv: ', argv
	if len(argv) != 2:
		print("Usage: python program.py source_directory destination_directory")
		return
	# 获取命令行参数
	MAP_DIR = argv[1]
	MAP_DIR = MAP_DIR.decode('utf-8')
	if not os.path.exists(MAP_DIR):
		print("Not is a directory")
	config = read_config()

	zh_lan_path = os.path.join(MAP_DIR, 'zhlanguage.json')
	zh_lan_data = _JsonObjHook(json.load( open(zh_lan_path, 'r'), encoding="utf-8"))
	en_lan_path = os.path.join(MAP_DIR, 'uslanguage.json')
	en_lan_data = _JsonObjHook(json.load(open(en_lan_path, 'r'), encoding="utf-8"))

	for table_name in config['tables']:
		gen_file_by_table(MAP_DIR, table_name, zh_lan_data, en_lan_data)

	zh_lan_data = json.dumps(hint_tuples(zh_lan_data), ensure_ascii=True, indent=4, encoding="utf-8")
	with open(zh_lan_path, 'w') as writter:
		writter.write(zh_lan_data)
	en_lan_data = json.dumps(hint_tuples(en_lan_data), ensure_ascii=True, indent=4, encoding="utf-8")
	with open(en_lan_path, 'w') as writter:
		writter.write(en_lan_data)
	print'Gen Json Data: '+ zh_lan_path
	print'Gen Json Data: '+ en_lan_path

if __name__ == "__main__":
	main(sys.argv)
