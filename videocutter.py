import cv2

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


startoffset=0
endoffset=0
fps=60
tolerance=30
startcoors=[]
endcoors=[]
startframe=0

capture=cv2.VideoCapture("file.mp4")

hasStarted=False
gamecount=0
startframe=0
endframe=0

def checkStarted(frame):
	for coor in startcoors:
		pixel=frame[coor[0][1],coor[0][0]]
#		print(pixel)
		for i in range(0,3):
			if abs(pixel[2-i]-coor[1][i])>tolerance:
				return False
	return True

def checkEnded(frame):
	for coor in endcoors:
		pixel=frame[coor[0][1],coor[0][0]]
		for i in range(0,3):
			if abs(pixel[2-i]-coor[1][i])>tolerance:
				return False
#		print(pixel)
	return True

while capture.isOpened():
	ret,frame=capture.read()
	if ret:
		#cv2.imwrite(f"frame{startframe}.jpg",frame)
		if not hasStarted:
			if checkStarted(frame):
				hasStarted= True
				startframe=startframe
				print(f"game started on frame {startframe}")
				#cv2.imwrite(f"started{startframe}.jpg",frame)
		if hasStarted:
			if checkEnded(frame):
				hasStarted=False
				endframe=startframe
				gamecount+=1
				ffmpeg_extract_subclip("file.mp4", startframe/fps+startoffset, endframe/fps+endoffset, targetname=f"output/game{gamecount}.mp4")
				print(f"game ended on frame {startframe}")
				#cv2.imwrite(f"ended{startframe}.jpg",frame)
		startframe+=60
#		print(startframe)
		capture.set(1,startframe)
	else:
		capture.release()
		break
