# CoreImage 裁剪核心图片
<br/>
##作用
核心图片：是指一张图片中最重要的部分。<br/>
目前适用于纯色背景图片截取和人物图片剪切<br>

##效果展示
人物原图<br/>
![github](https://github.com/george518/CoreImage/blob/master/originalImage/face.jpg?raw=true "github")
<br/><br/>
截取280*280大小大图片。效果如下：<br/>
![github](https://github.com/george518/CoreImage/blob/master/newImage/new_face.jpg?raw=true "github")
<br/><br/>
纯背景图片<br/>
![github](https://github.com/george518/CoreImage/blob/master/originalImage/image.jpg?raw=true "github")
<br/><br/>
去除背景。效果如下：<br/>
![github](https://github.com/george518/CoreImage/blob/master/newImage/new_image.jpg?raw=true "github")
<br/>

##环境
python3.4.3<br/>
openCv3.1.0<br/>

##Mac安装过程
brew install opencv3 --with-python3<br/>
brew unlink opencv<br/>
brew ln opencv3 --force<br/>
ln -s /usr/local/Cellar/opencv/2.4.12_2/lib/python2.7/site-packages/cv2.so cv2.so<br>

