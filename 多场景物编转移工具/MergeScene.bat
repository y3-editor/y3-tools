@echo off

echo Please input the location of warcraft root folder, e.g.:
REM 设置arg1为美术地图路径，arg2为逻辑地图路径
set "arg1=F:\ST1\assets\scenes\12.15\ST1\maps\EntryMap"
set "arg2=F:\ST1\master\maps\EntryMap"

REM 调用 Python 脚本并传递参数
python main.py %arg1% %arg2%
pause