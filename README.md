## Preview

***QR-TrashCan***  是一台能便于用户垃圾分类与政府处理各类垃圾的垃圾桶，并且管理员能对其进行监控。

***QR-TrashCan***  的构想：

- 存在两个现象：
    - 居民无法自觉分类而导致随意乱扔
    - 居民对各种垃圾的分类不明确，导致勿扔。全民科普又不现实，效果也欠佳
- ***QR-TrashCan*** 的解决方案：
    - 在每个垃圾上都设有与之对应的二维码，此二维码由政府和企业协商，合作推行
    - 用户将二维码对准垃圾桶上的摄像头，自动打开相应的垃圾桶盖
- 管理方案：
    - [x] 可在浏览器上查看摄像头实时影像
    - [x] 只有注册用户能登录查看与监控
    - [ ] 后台可查看各垃圾区域的垃圾数量
    - [x] 生成二维码

## 外形与功能展示

1. 实物图

| <img src="/img/img_8.jpg" style="zoom:10%;" /> | <img src="/img/img_9.jpg" style="zoom:10%;" /> |
| :----------------------------------------------------------: | :------------------------------------: |
| <img src="/img/img_1.jpg" style="zoom:10%;" /> | <img src="/img/img_5.jpg" style="zoom:10%;" /> |



1. 登录界面

<img src="/img/img_2.png" style="zoom:15%;" />

<img src="/img/img_3.png" style="zoom:15%;" />

<img src="/img/img_4.png" style="zoom:15%;" />


## 准备工作
***所需材料***
<center>

|   设备           |     数量   |
| :-------------: | :--------: |
| 树莓派4B+        |      1     |
| CSI摄像头        |      1     |
|   舵机           |      4     |
|   外壳           |      1     |
	
</center>	

## 环境搭建
1. 一共分为3步骤

2. 详细步骤：
    - 虚拟环境与二维码部分

        ```bash
        pip install virtualenv 
        pip install qrcode
        pip install Image
        cd ~/Desktop
        virtualenv -p python3 venv
        ```

    - Flask
    
        ```bash
        pip install flask
        pip install flask-wtf
        pip install flask-SQLAlchemy
        pip install flask-Bcrypt
        pip install flask-login
        pip install wtforms
        ```

    - 舵机模块

        - *开启I2C并下载 i2c-tool*
    
            ```bash
            sudo raspi-config
            sudo apt-get install i2c-tools
            ```
        
            依次选择“Interfacing Options”-“P5 I2C”—“yes”—“ok”
        
            ```bash
            lsmod
            ```
        
            查看I2C是否成功启动
	    
        - *下载Adafruit-PCA9685驱动*
    	
            ```bash
            sudo apt-get update
            sudo apt-get install build-essential python-pip python-dev python-smbus git
            git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git
            ```
        
            在终端中依次输入
        
            ```bash
            cd Adafruit_Python_PCA9685
            sudo python setup.py install
            ```
        
            检测BST-AI占用的IIC地址，在终端中输入
        
            ```bash
            i2cdetect -y -a 1
            ```
        
            查找前驱动板的地址。如图所示当前驱动板i2c地址为0x41， 进入piAdafruit_Python_PCA9685Adafruit_PCA9685/PCA9685.py将参数PCA9685_ADDRESS的值改为0x41：
            
            <img src="/img/img_11.jpg" style="zoom: 50%;" />
## 启动

- 创建数据库

    在项目的根目录下，新建一个文件，database.db2 ，利用shell打开python

    ```python
    from app import db
    db.create_all()
    ```

    查看相应的表是否建立，这里使用DB Browser：

    <img src="/img/img_6.png" style="zoom:50%;" />

- 生成二维码：

    - 修改generator.py中L列表，填上所需要分类的垃圾的名称
    - 运行generator.py, 会在项目的根目录生成相应的二维码

    <img src="/img/img_12.png" style="zoom:33%;" />

    

- 启动服务器

    ```bash
    cd ~/Desktop/venv
    python3 app.py
    ```

- 打开电脑，连接同一WiFi或热点，在浏览器中输入相应的url，端口号为5000

    ```bash
    sudo ifconfig | grep inet
    ```

<img src="/img/img_7.png" style="zoom:38%;" />

<img src="/img/img_8.png" style="zoom:38%;" />

