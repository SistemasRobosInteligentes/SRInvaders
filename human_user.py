#packages for computer vision
import cv2
import mediapipe as mp
import math
from screeninfo import get_monitors


class human_user:
    def __init__(self,screen_width):
        self.screen_width = screen_width
        self.image_mat = []
        self.x_pos = screen_width/2 - 16
        self.may_shoot = False
        self.pull_string = False
        self.squat = False
        self.camera_width = 600
        self.camera_height = 450
        self.camera_on = False
        
    def camera(self, cap):
                
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        
        with mp_pose.Pose(
            min_detection_confidence=0.75,
            min_tracking_confidence=0.5) as pose:
          
          if cap.isOpened():
            success, image = cap.read()
            
            self.camera_width = image.shape[1]
            self.camera_height = image.shape[0]
            
          while cap.isOpened():
            success, image = cap.read()
                        
            if not success:
              print("Ignoring empty camera frame.")
              # If loading a video, use 'break' instead of 'continue'.
              continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Flip the image horizontally for a selfie-view display.
            
            #image = image[0:image.shape[0],rows_to_ignore:(image.shape[1] - rows_to_ignore),0:image.shape[2]]
            
            #truncar em altura
            #image = image[rows_to_ignore:(image.shape[0] - rows_to_ignore),0:image.shape[1],0:image.shape[2]]
            
            if self.camera_on:
                image = cv2.resize(image,(int(self.camera_width),int(self.camera_height)))
                #image = image[rows_to_ignore:(image.shape[0] - rows_to_ignore),0:image.shape[1],0:image.shape[2]]
                
                
            self.image_mat = image
            
            try:
                if results.pose_landmarks.landmark[11].x > 0 and results.pose_landmarks.landmark[11].x < 1 and results.pose_landmarks.landmark[12].x > 0 and results.pose_landmarks.landmark[12].x < 1 and results.pose_landmarks.landmark[23].x > 0 and results.pose_landmarks.landmark[23].x < 1 and results.pose_landmarks.landmark[24].x > 0 and results.pose_landmarks.landmark[24].x < 1:
                    calculated_x = self.screen_width - math.floor(((results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x + results.pose_landmarks.landmark[23].x + results.pose_landmarks.landmark[24].x)*self.screen_width/4))
                    self.x_pos = round((calculated_x - 65*self.screen_width/1920)*self.screen_width/(self.screen_width-130*self.screen_width/1920))
                    if self.x_pos < 0:
                        self.x_pos = 0
                    elif self.x_pos > self.screen_width - round(32*self.screen_width/1920):
                        self.x_pos = self.screen_width - round(32*self.screen_width/1920)
                #else:
                    #self.x_pos = self.screen_width/2 - 16
                    
            except AttributeError:
                print("No pose found")
                #self.x_pos = self.screen_width/2 - 16
            if results.pose_landmarks is not None:
                ratioright = results.pose_landmarks.landmark[24].y/results.pose_landmarks.landmark[26].y
                ratioleft = results.pose_landmarks.landmark[23].y/results.pose_landmarks.landmark[25].y
                if ratioright > 0.72 or ratioleft > 0.72:
                    self.squat = True
                    
                    
            
            if self.may_shoot==True:
                self.pull_string=False
                
            try:
                if (results.pose_landmarks.landmark[20].y > 0 and results.pose_landmarks.landmark[20].y < 1 and results.pose_landmarks.landmark[12].x > 0 and results.pose_landmarks.landmark[12].x < 1) or (results.pose_landmarks.landmark[19].y > 0 and results.pose_landmarks.landmark[19].y < 1 and results.pose_landmarks.landmark[11].x > 0 and results.pose_landmarks.landmark[11].x < 1):
                  if results.pose_landmarks.landmark[20].y > results.pose_landmarks.landmark[12].y and results.pose_landmarks.landmark[19].y > results.pose_landmarks.landmark[11].y:  
                      self.pull_string = True
                      
                  if results.pose_landmarks.landmark[20].y < results.pose_landmarks.landmark[12].y and self.pull_string == True or results.pose_landmarks.landmark[19].y < results.pose_landmarks.landmark[11].y and self.pull_string == True:
                        self.may_shoot = True
                        #print((results.pose_landmarks.landmark[24].y)/(results.pose_landmarks.landmark[26].y)) 
                  else:
                            self.may_shoot = False
                            
                else: 
                    self.may_shoot = False
                    
                
            except AttributeError:
                self.may_shoot = False
  
