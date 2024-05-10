# -*- coding: utf-8 -*-
"""
@file：json_helper
@description:
@author: longyunyue@corp.netease.com
@date：2024/2/29
"""
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