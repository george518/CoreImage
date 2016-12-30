# -*- coding: utf-8 -*-
# @Author: haodaquan
# @Date:   2016-12-25 10:13:57
# @Last Modified by:   haodaquan
# @Last Modified time: 2016-12-30 16:50:36
import sys
import copy
import cv2
import math

#----------------------------------------------------------------------  
# CoreImage: 核心图片类，获取核心图片
#----------------------------------------------------------------------  
class CoreImage(object):
	#imageInfo = [imageName,imagePath,newImagePath]
	def __init__(self,*arg):
		imgInfo  = arg[0]
		cropInfo = arg[1]
		#原图信息
		self.imgPath    = imgInfo.get('imgPath','./originalImage/')
		self.imgName    = imgInfo.get('imgName','image.jpg')

		#新图信息
		self.newImgPath = cropInfo.get('newImgPath','./newImage/')
		self.isBgPure   = cropInfo.get('isBgPure',0)#是否纯色背景，0-不是，1-是
		self.newWidth   = cropInfo.get('newWidth',380)
		self.newHeight  = cropInfo.get('newHeight',380)


	#获取图片边缘
	def getImgEdge(self):
		img  = cv2.imread(self.imgPath+self.imgName)
		edge = cv2.Canny(img,100,300) #可以根据实际业务进行调整
		# cv2.imwrite(self.newImgPath+'edge.jpg',edge)
		return [edge,img]

	#获取核心图片
	def getCoreImg(self):
		if(self.isBgPure==1):
			return self.getPureBgCoreImg()
		else:
			return self.getDefaultBgCoreImg()

	#获取纯色背景核心图片
	def getPureBgCoreImg(self):
		edgeImg = self.getImgEdge()
		img_width = edgeImg[1].shape[1]
		img_height = edgeImg[1].shape[0]
		x0 = 0 # 左上角x
		y0 = 0 # 左上角y
		x1 = img_width-1
		y1 = img_height-1

		i = j = 0
		for i in range(0,img_width):
			if(x0!=0):
				break;
			for j in range(0,img_height):
				if(edgeImg[0][j,i]!=0):
					x0=i
					break
		i = j = 0
		for i in range(0,img_height):
			if(y0!=0):
				break;
			for j in range(0,img_width):
				if(edgeImg[0][i,j]!=0):
					y0=i
					break
		i = j = 0
		for i in range(0,img_width)[::-1]:
			if(x1!=img_width-1):
				break;
			for j in range(0,img_height)[::-1]:
				if(edgeImg[0][j,i]!=0):
					x1=i
					break
		i = j = 0
		for i in range(0,img_height)[::-1]:
			if(y1!=img_height-1):
				break;
			for j in range(0,img_width)[::-1]:
				if(edgeImg[0][i,j]!=0):
					y1=i
					break
		crop_img = edgeImg[1][y0:y1,x0:x1]
		cv2.imwrite(self.newImgPath+'new_image.jpg',crop_img)
		return crop_img

	#获取默认的核心图片 含人脸识别
	def getDefaultBgCoreImg(self):
		# 加载训练好的脸、眼分类器
		face_cascade = cv2.CascadeClassifier(
	    	'/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
		eye_cascade = cv2.CascadeClassifier(
			'/usr/local/share/OpenCV/haarcascades/haarcascade_eye.xml')

		width  = self.newWidth
		height = self.newHeight

		img = cv2.imread(self.imgPath+self.imgName)
		# 返回 img 的浅拷贝
		original = copy.copy(img)
	    # 转换为灰度图
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	    # 检测人脸
		faces = face_cascade.detectMultiScale(
	    	gray,
	    	scaleFactor=1.1,
	    	minNeighbors=5,
	    	minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE)

		imHeight, imWidth = img.shape[:2]
		maxFaceCenter = 0
		maxFaceRight  = 0
		maxFaceMidlle = 0

		for (x, y, w, h) in faces:
			# 人脸部分用实心矩形框选
			cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)
			# cropBias = cropBias - x
			# 找出最大人脸
			if (x + w) > maxFaceRight:
				maxFaceCenter = (x + w) - (w // 2)
				maxFaceRight  = x + w
				maxFaceMidlle = y + h // 2
			# 截出人脸
			roi_gray = gray[y:y + h, x:x + w]
			roi_color = img[y:y + h, x:x + w]
			# 检测眼睛
			eyes = eye_cascade.detectMultiScale(roi_gray)
			# 框选出人眼
			for (ex, ey, ew, eh) in eyes:
				cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0),2)

		#左上角位置定位
		leftPosX = maxFaceCenter - width // 2
		leftPosY = maxFaceMidlle - height // 2
		if(leftPosX < 0):
			leftPosX = 0
		if(leftPosY < 0):
			leftPosY = 0
		# print(leftPosY,height, leftPosX,width)
		copyX = width + leftPosX
		copyY = height + leftPosY

		if(copyX < maxFaceRight):
			copyX = maxFaceRight

		# print(leftPosY,copyY, leftPosX,copyX)
		croppedData = original[leftPosY:copyY, leftPosX:copyX]
		croppedName = self.newImgPath+"new_face.jpg"
		cv2.imwrite(croppedName, croppedData)


if __name__ == '__main__':
	imgPath    = './originalImage/'
	newImgPath = './newImage/'
	
	#人脸识别
	imgName    = 'face.jpg'
	imgInfo = {'imgName':imgName,'imgPath':imgPath}
	newImgInfo = {'isBgPure':0,'newWidth':280,'newHeight':280};
	coeImg = CoreImage(imgInfo,newImgInfo)
	coeImg.getCoreImg();



	#背景纯色图
	imgName    = 'image.jpg'
	imgInfo = {'imgName':imgName,'imgPath':imgPath}
	newImgInfo = {'isBgPure':1};

	coeImg = CoreImage(imgInfo,newImgInfo)
	coeImg.getCoreImg();
	# imageEdge(imgpath)



		