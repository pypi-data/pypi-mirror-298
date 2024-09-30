# -*- coding: utf-8 -*-  
import sys
import os
import subprocess
import time
from ctypes import c_int
from setuptools import setup
from setuptools.command.install import install  # 修改导入语句
import atexit
import platform


# 该函数将在 Python 解释器正常终止时自动调用
def custom_action():
    print('Custom installation completed.')

# 注册自定义函数，使其在 Python 解释器正常终止时调用
atexit.register(custom_action)


if "win" in sys.platform:
    install_requires=['pyserial',
        'Pillow',
        'freetype-py==2.1.0',
        'modbus-tk==1.1.2'
        ]
else:
    install_requires=['pyserial',
        'Pillow',
        'smbus',
        #'smbus2',
        'spidev',
        'freetype-py==2.1.0',
        'evdev',
        'modbus-tk==1.1.2'
        ]

with open('README.md') as f:
    long_description = f.read()

# 自定义的install命令
class CustomInstall(install):
    def run(self):
        # 调用父类的run方法以确保正常安装
        install.run(self)
        # 只匹配unihiker
        if platform.node() == "unihiker":
            self.init_script()
        
    def init_script(self):
        print('pip install  test  print')
        time.sleep(1)
        # 获取当前文件的绝对路径
        current_directory = os.path.dirname(__file__)
        print('path: ', current_directory)
        # 构建新的文件路径
        gd32_script = os.path.join(current_directory, "build", "lib", "pinpong", "base", "gd32", "burn.sh")
        setup_script = os.path.join(current_directory, "build", "lib", "pinpong", "base", "gd32", "setup.sh")
        anaysis_script = os.path.join(current_directory, "build", "lib", "pinpong", "base", "gd32", "anaysis.py")
        
        print('gd32_script : ', gd32_script)
        
        print('setup_script : ', setup_script)
        try:
            os.chmod(gd32_script, 0o777)
            os.chmod(setup_script, 0o777)
            subprocess.run(["bash", gd32_script])
            print('anaysis_script : ', anaysis_script)
            #subprocess.run(["python", anaysis_script])
            subprocess.run(["bash", setup_script])
        except Exception:
            print("install error: ")
            
        

setup(
    name='pinpong',
    packages=['pinpong','pinpong/base','pinpong/libs','pinpong/examples','pinpong/examples/xugu','pinpong/examples/nezha','pinpong/examples/RPi','pinpong/examples/handpy','pinpong/examples/microbit','pinpong/examples/UNIHIKER','pinpong/examples/win','pinpong/extension/','pinpong/examples/PinPong Board/','pinpong/examples/PinPong Board/example/Many_board_control','pinpong/examples/PinPong Board/example/serial_example','pinpong/examples/PinPong Board/example/tcp_example','pinpong/base/gd32'],
    install_requires=install_requires,

    include_package_data=True,
    entry_points={
        "console_scripts":["pinpong = pinpong.base.help:main"],
    },
    version='0.6.0',
    description="一个纯python实现的支持丰富外设的驱动库，支持win linux mac系统，支持arduino系列开发板，RPi、D1等linux开发板。附带丰富的使用例程",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    author='Ouki Wang',
    author_email='ouki.wang@dfrobot.com',
    url='https://github.com/DFRobot/pinpong-docs',
    download_url='https://github.com/DFRobot/pinpong-docs',
    keywords=['Firmata', 'Arduino', 'Protocol', 'Python'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    
    cmdclass={'install': CustomInstall},

)
