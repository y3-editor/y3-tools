# -*- coding: utf-8 -*-
import os
import shutil
import sys


def _JsonObjHook(x):
	"""
	工具方法,用于json.loads的object_hook
	1.为了保证键还是int
	2.还原出tuple
	3.保证转换unicode
	"""
	if type(x) is dict:
		ret_obj = {}
		# 检测此dict是否为tuple
		if '__tuple__' in x and x['__tuple__']:
			return tuple(_JsonObjHook(x['items']))
		for k, v in x.items():
			real_key = k
			try:
				# 直接尝试转换为int，如果转换不了就算了
				real_key = int(real_key)
			except:
				# 转换失败，需要unicode解码
				if type(real_key) is unicode:
					real_key = real_key.encode("utf8")
			try:
				if type(v) is unicode:
					v = v.encode("utf8")
				elif type(v) in (dict, list):
					# 继续向下递归处理所有的dict
					v = _JsonObjHook(v)
			except:  # noqa
				pass

			ret_obj[real_key] = v
		return ret_obj
	elif type(x) is list:
		# 对于list，需要遍历一下内容，让其中的unicode字符串强行转换为utf8
		for x_index, x_value in enumerate(x):
			if type(x_value) is unicode:
				x[x_index] = x_value.encode("utf8")
			elif type(x_value) in (list, dict):
				x[x_index] = _JsonObjHook(x_value)
	return x


def hint_tuples(item):
	""" 将数据中的tuple封装,用于json.dumps """
	if isinstance(item, tuple):
		return {'__tuple__': True, 'items': item}
	if isinstance(item, list):
		return [hint_tuples(e) for e in item]
	if isinstance(item, dict):
		tmp = {}
		for key, value in item.iteritems():
			# 出现形如'123'的key,report
			if isinstance(key, basestring) and key.isdigit():
				print 'digit_str key(%s), invalid data type' % key
			tmp[key] = hint_tuples(value)
		return tmp
	else:
		return item


FILES = [
	"decal.json",
	"decorationdata.data",
	"engineeffectdata.json",
	"envtime.json",
	"foliage.json",
	"navimap.data",
	"resourceobjectdata.data",
	"terrain.json",
	"terrainedit.json",
	"todtemplate.json",
	"editor/folderinfo/folderinfo_editor_decoration.json",
	"editor_table/editordecoration",
	"texturefoliage.json",
	"texture.json",
	"projectile.json"
]


def gen_2_power(idx=0):
	if idx > 32:
		raise ValueError("%s is too large to gen_logic_unit_type_id" % idx)
	return 2 ** idx


LOGIC_RES_MASTER = [
	10, 11, 12, 13, 15, 16, 19, 21, 22
]


def replace_files_in_folder(src_dir, dst_dir):
	# 获取源文件夹中的所有文件
	filenames = os.listdir(src_dir)

	# 遍历所有文件
	for filename in filenames:
		src_file = os.path.join(src_dir, filename)
		dst_file = os.path.join(dst_dir, filename)

		# 检查文件是否存在
		if os.path.exists(dst_file):
			# 删除目标文件
			os.remove(dst_file)

		print('replace file: ' + src_file + 'to: ' + dst_file)
		# 复制源文件到目标文件夹
		shutil.copy(src_file, dst_file)


def replace_files(src_dir, dst_dir):
	for filename in FILES:
		src_file = os.path.join(src_dir, filename)
		dst_file = os.path.join(dst_dir, filename)
		print 'src_file: ', src_file
		print 'dst_file: ', dst_file
		if os.path.isdir(src_file) and os.path.isdir(dst_file):
			replace_files_in_folder(src_file, dst_file)
		elif os.path.exists(src_file) and os.path.exists(dst_file):
			print 'replace file: ' + src_file + 'to: ' + dst_file
			shutil.copy2(src_file, dst_file)  # 复制源文件到目标文件


def process_logic_res(art_dir, master_dir):
	import json
	art_logic_res = os.path.join(art_dir, 'logicres.json')
	master_logic_res = os.path.join(master_dir, 'logicres.json')
	art_file = open(art_logic_res)
	master_file = open(master_logic_res)
	art_data = _JsonObjHook(json.load(art_file, encoding="utf-8"))
	master_data = _JsonObjHook(json.load(master_file, encoding="utf-8"))
	diff = {}
	for idx in LOGIC_RES_MASTER:
		key = gen_2_power(idx)
		if key in master_data:
			diff[key] = master_data[key]
	art_data.update(diff)
	json_data = json.dumps(hint_tuples(art_data), ensure_ascii=True, indent=4,
						   sort_keys=True)
	master_file.close()
	art_file.close()
	with open(os.path.abspath(master_logic_res), 'w') as writter:
		writter.write(json_data)
	print 'process_logic_res done'


def main(argv):
	# 检查命令行参数的数量
	print 'argv: ', argv
	if len(argv) != 3:
		print("Usage: python program.py source_directory destination_directory")
		return

	# 获取命令行参数
	src_dir = argv[1]
	src_dir = src_dir.decode('utf-8')
	dst_dir = argv[2]
	dst_dir = dst_dir.decode('utf-8')

	# 执行文件替换操作
	replace_files(src_dir, dst_dir)
	process_logic_res(src_dir, dst_dir)

if __name__ == "__main__":
	main(sys.argv)
