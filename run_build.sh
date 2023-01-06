#!/bin/bash
echo "清理文件......"
rm -r dist/out
echo "开始编译......"


# MAC 方案1 成功
# 必须使用对应版本的pyinstall
# 必须使用 import cv2 ; print(cv2.__file__) 打印的路径来设置--path参数，否则 打包后缺少 模块 cv2
# ImportError: OpenCV loader: missing configuration file: ['config.py']. Check OpenCV installation.
# 解决 opencv4.5.5 升级到4.6.0.66,pyinstaller 4.8升级到 5.3 解决缺少cv2和config.py的问题
# pip3 install --upgrade pyinstaller==5.3
/Users/luge/opt/anaconda3/envs/pythonenv37/bin/pyinstaller -F -i ichat.ico -w --windowed --noconsole --onefile --clean --noconfirm --hidden-import opencv-python --hidden-import opencv --hidden-import cv2 --paths="/Users/luge/opt/anaconda3/envs/pythonenv37:/Users/luge/opt/anaconda3/envs/pythonenv37/bin:/Users/luge/opt/anaconda3/envs/pythonenv37/lib/python3.7/site-packages/cv2" start.py
/Users/luge/opt/anaconda3/envs/pythonenv37/bin/pyinstaller --clean --noconfirm --windowed --onefile start.spec

# MAC 方案2 --qt-plugins
#py2applet --make-setup start.py --iconfile ./ichat.ico --alias Ios控制台
#python3 setup.py py2app

echo "编译结束"
echo "复制文件......"
#mkdir dist/out
cp ./config.ini dist/config.ini
#cp dist/userctrl dist/out/Ios控制台
#echo "复制结束"
