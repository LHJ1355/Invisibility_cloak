import cv2
import numpy as np
import time
import camera

class ColorDetect():
    def __init__(self):
        self.camera = camera.VideoCamera()
        self.background = 0
        
        #특정 색깔에 mask를 씌우기 위해 범위 설정
        self.lower_blue = np.array([94, 80, 2])
        self.upper_blue = np.array([126, 255, 255])
        
    def __del__(self):
        del self.camera

    #background이미지 생성
    def make_background(self):  
        time.sleep(3)
        for k in range(45):
            background = self.camera.get_frame()
            
        #flip는 배열 뒤집기
        self.background = np.flip(background,axis=1)
        
    #매 프레임마다 특정한 색 부분을 background이미지와 합성한 이미지를 return
    def get_frame(self):
        frame = self.camera.get_frame()
        frame = np.flip(frame, axis=1)
        #bgr이미지를 hsv이미지로 convert
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #hsv이미지에서 특정 색 부분을 식별해 mask_all로 설정
        mask_all = cv2.inRange(hsv,self.lower_blue,self.upper_blue)
        
        #mask_all을 보간
        mask_all = cv2.morphologyEx(mask_all, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        mask_all = cv2.morphologyEx(mask_all, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
        
        #특정 색 이외의 부분을 mask2로 설정
        mask2 = cv2.bitwise_not(mask_all)
        
        #특정 색 이외의 부분만 표시되는 이미지 streamA
        streamA = cv2.bitwise_and(frame,frame,mask=mask2)

        #background이미지에서 각 frame의 특정 색 부분만 추출한 이미지 streamB
        streamB = cv2.bitwise_and(self.background, self.background, mask = mask_all)
 
        #streamA 와 streamB를 동일한 가중치를 가지고 합성
        output = cv2.addWeighted(streamA,1,streamB,1,0)
        return output
        
    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


if __name__ == '__main__':
    color_detect = ColorDetect();
    color_detect.make_background()

    while True:
        frame = color_detect.get_frame()

        # 매 프레임 출력
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  #esc키 클릭시 종료, 다른 알파벳 키를 클릭했을때 종료하고싶다면 "if key == ord('q'):" 사용. q클릭시 종료 
            break


    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')
# ## Notes for adding colors

# ###### Red color
# low_red = np.array([161, 155, 84])
# high_red = np.array([179, 255, 255])
# red_mask = cv2.inRange(hsv_frame, low_red, high_red)
# red = cv2.bitwise_and(frame, frame, mask=red_mask)
# 
# ###### Blue color
# low_blue = np.array([94, 80, 2])
# high_blue = np.array([126, 255, 255])
# blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
# blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
# 
# ###### Green color
# low_green = np.array([25, 52, 72])
# high_green = np.array([102, 255, 255])
# green_mask = cv2.inRange(hsv_frame, low_green, high_green)
# green = cv2.bitwise_and(frame, frame, mask=green_mask)
# 
# ###### Every color except white
# low = np.array([0, 42, 0])
# high = np.array([179, 255, 255])
# mask = cv2.inRange(hsv_frame, low, high)
# result = cv2.bitwise_and(frame, frame, mask=mask)
