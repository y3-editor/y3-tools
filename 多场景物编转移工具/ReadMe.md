使用说明:.
使用前需要安装python2.7版本。安装流程可见：https://blog.csdn.net/zzfenglin/article/details/52336440
这个工具用来从主关卡向其他子关卡进行合并数据,目前仅支持物编表,注意,使用工具前请先备份,并且关闭项目工程
另外包含属性定义面板中的数据:玩家属性,单位属性,复合属性,经验公式,伤害公式
1.右键使用记事本方式打开Run.bat，修改arg1=后面的路径为物编主关卡的地图路径。

2.在config中配置需要合并的物编表名

3.注意:目录信息会用主关卡的全量覆盖其他子关卡

ps:物编表对应关系

```
teable_name = {
    'editor_unit': '单位',
    'editor_decoration': '装饰物',
    'editor_item': '物品',
    'projectile_all': '投射物',
    'ability_all': '技能',
    'technology_all': '科技',
    'editor_destructible': '可破坏物',
    'sound_all': '声音',
    'modifier_all': '魔法效果',
}
```

4.有bug联系或者二次开发需求longyunyue@corp.netease.com


编辑器交流群:龙云跃