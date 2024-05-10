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


def copy_dir(src, dst):
	"""
	复制目录（合并patch和pkg下的数据，两边都有时优先patch里的）
	:param src:
	:param dst:
	:return:
	"""
	for root, dirs, files in os.walk(src):
		for file in files:
			source_file_path = os.path.join(root, file)  # 源文件路径
			destination_file_path = os.path.join(dst, file)  # 目标文件路径
			shutil.copy(source_file_path, destination_file_path)  # 拷贝文件


def read_config():
	config_file = os.path.join(os.path.dirname(__file__), 'config.json')
	config = json.load(open(config_file))
	return config


def get_localize_tid(hash_key):
	from src.utils.hash_helper import hash_func
	return hash_func(str(hash_key))


def get_sub_levels(main_level):
	r = []
	parent_folder = os.path.dirname(main_level)
	for sub_level_name in os.listdir(parent_folder):
		sub_level = os.path.join(parent_folder, sub_level_name)
		main_level = os.path.normpath(main_level)
		sub_level = os.path.normpath(sub_level)
		if os.path.isdir(sub_level) and main_level != sub_level:
			r.append(sub_level)
	for sub_dir in r:
		print 'sub_dir: ', sub_dir
	return r


TABLE_NAME_TO_TRIGGER_FOLDER = {
	'editor_unit': 'unit',
	'ability_all': 'ability',
	'editor_item': 'item',
	'modifier': 'modifier',
	'destructible': 'destructible',
	'projectile_all': 'projectile',
}


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


def merge_attr_data(main_level, sub_level):
	src_dst =  os.path.join(main_level, 'attr.json')
	dst_dst =  os.path.join(sub_level, 'attr.json')
	shutil.copy(src_dst, dst_dst)
	print 'Copy attr data from ', src_dst, ' to ', dst_dst


def merge_damage_data(main_level, sub_level):
	src_dst =  os.path.join(main_level, 'damage.json')
	dst_dst =  os.path.join(sub_level, 'damage.json')
	shutil.copy(src_dst, dst_dst)
	print 'Copy damage data from ', src_dst, ' to ', dst_dst



def merge_rule_data(main_level, sub_level):
	rule_keys = [1,3, 108, 114, 415, 416, 417, 426, 427]
	src_dst =  os.path.join(main_level, 'ruledata.json')
	dst_dst =  os.path.join(sub_level, 'ruledata.json')
	shutil.copy(src_dst, dst_dst)
	src_json_data = json.load(open(src_dst, 'r'), encoding="utf-8")
	dst_json_data = json.load(open(dst_dst, 'r'), encoding="utf-8")
	for k in rule_keys:
		if k in src_json_data:
			dst_json_data[k] = src_json_data[k]
	with open(dst_dst, 'w') as writter:
		writter.write(json.dumps(hint_tuples(dst_json_data), ensure_ascii=True, indent=4, encoding="utf-8"))
	print 'Merge exp data from ', src_dst, ' to ', dst_dst



def merge_file_by_table(main_level, table_name, zh_lan_data, en_lan_data):
	# 物编数据
	data_folder = os.path.join(main_level, 'editor_table', table_name.replace('_', ''))
	print 'data_folder: ', data_folder
	sub_levels = get_sub_levels(main_level)
	tids = set()
	for sub_level in sub_levels:
		sub_data_folder = os.path.join(sub_level, 'editor_table', table_name.replace('_', ''))
		copy_dir(data_folder, sub_data_folder)
		print 'Copy data from ', data_folder, ' to ', sub_data_folder
		files = os.listdir(data_folder)
		# 触发器数据
		if table_name in TABLE_NAME_TO_TRIGGER_FOLDER:
			prefix = TABLE_NAME_TO_TRIGGER_FOLDER.get(table_name)
			for file_name in files:
				src_trigger_file = os.path.join(main_level, prefix, file_name)
				if os.path.exists(src_trigger_file):
					dst_trigger_file = os.path.join(sub_level, TABLE_NAME_TO_TRIGGER_FOLDER.get(table_name), file_name)
					shutil.copy(src_trigger_file, dst_trigger_file)
					print 'Copy trigger file: ', src_trigger_file, ' to ', dst_trigger_file
		if table_name in hash_prefix_map:
			for file_name in files:
				has_prefix = hash_prefix_map.get(table_name)
				name_hash_key = has_prefix + '_' + file_name.replace('.json', '') + '_' + 'name'
				desc_hash_key = has_prefix + '_' + file_name.replace('.json', '') + '_' + 'desc'
				tids.add(get_localize_tid(name_hash_key))
				tids.add(get_localize_tid(desc_hash_key))
		# 多语言
		zh_language_path  = os.path.join(sub_level, 'zhlanguage.json')
		us_language_path = os.path.join(sub_level, 'uslanguage.json')
		sub_zh_lan_data = _JsonObjHook(json.load( open(zh_language_path, 'r'), encoding="utf-8"))
		sub_en_lan_data = _JsonObjHook(json.load(open(us_language_path, 'r'), encoding="utf-8"))
		for tid in tids:
			sub_zh_lan_data[tid] = zh_lan_data.get(tid, str(tid))
			sub_en_lan_data[tid] = en_lan_data.get(tid, str(tid))
		sub_zh_lan_data = json.dumps(hint_tuples(sub_zh_lan_data), ensure_ascii=True, indent=4, encoding="utf-8")
		with open(zh_language_path, 'w') as writter:
			writter.write(sub_zh_lan_data)
		print 'Write zh language data to ', zh_language_path
		sub_en_lan_data = json.dumps(hint_tuples(sub_en_lan_data), ensure_ascii=True, indent=4, encoding="utf-8")
		with open(us_language_path, 'w') as writter:
			writter.write(sub_en_lan_data)
		print 'Write en language data to ', us_language_path
		# 目录信息
		src_folder_path = os.path.join(main_level, 'editor', 'folderinfo', 'folderinfo_'+ table_name + '.json')
		dst_folder_path = os.path.join(sub_level, 'editor', 'folderinfo', 'folderinfo_'+ table_name + '.json')
		if os.path.exists(src_folder_path):
			shutil.copy(src_folder_path, dst_folder_path)
			print 'Copy folder info from ', src_folder_path, ' to ', dst_folder_path
		# 属性定义
		merge_attr_data(main_level, sub_level)
		# 攻防属性
		merge_damage_data(main_level, sub_level)
		# 规则数据
		merge_rule_data(main_level, sub_level)

def merge_global_trigger(main_level):
	sub_levels = get_sub_levels(main_level)
	for sub_level in sub_levels:
		src_trigger_path = os.path.join(main_level, 'global_trigger', )
		if os.path.exists(src_trigger_path):
			dst_trigger_path = os.path.join(sub_level, 'global_trigger')
			shutil.rmtree(dst_trigger_path.encode('gbk'))
			shutil.copytree(src_trigger_path.encode('gbk'), dst_trigger_path.encode('gbk'))


def main(argv):
	# 检查命令行参数的数量
	print 'argv: ', argv
	if len(argv) != 2:
		print("Usage: python program.py source_directory destination_directory")
		return
	# 获取命令行参数
	main_level = argv[1]
	main_level = main_level.decode('utf-8')
	print 'main_level: ', main_level
	if not os.path.exists(main_level):
		print("Not is a directory: ", main_level)
	config = read_config()

	zh_lan_path = os.path.join(main_level, 'zhlanguage.json')
	zh_lan_data = _JsonObjHook(json.load( open(zh_lan_path, 'r'), encoding="utf-8"))
	en_lan_path = os.path.join(main_level, 'uslanguage.json')
	en_lan_data = _JsonObjHook(json.load(open(en_lan_path, 'r'), encoding="utf-8"))

	for table_name in config['tables']:
		merge_file_by_table(main_level, table_name, zh_lan_data, en_lan_data)
	if 'global_trigger' in config and config['global_trigger']:
		merge_global_trigger(main_level)


if __name__ == "__main__":
	main(sys.argv)
