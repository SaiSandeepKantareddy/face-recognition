import face_recognition
import cv2
import os
import time
# This is a demo of blurring faces in video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(-1)

# Initialize some variables
face_locations = []
frames=0

temp=[]
p={}


def locations_compare(a,b):
    if (abs(a[0]-b[0])<=10 and abs(a[1]-b[1])<=10 and abs(a[2]-b[2])<=10 and abs(a[3]-b[3])<=10):
        return True
    else: 
        return False

def extend_boundaries(top,right,bottom,left,offset,height,width):
    a,c,b,d = top,right,bottom,left
    B = int(b+((b-a)*offset))
    D = int(d -((c-d)*offset))
    A = int(a -((b-a)*offset))
    C = int(c +((c-d)*offset))
    if B >height:
        B = height
    if D <0:
        D = 0
    if A < 0:
        A = 0
    if C > width:
        C = width
    extended_face = [A,C,B,D]
    return extended_face
#start=time.time()
#print(start)
while frames<15:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    # Resize frame of video to 1/4 size for faster face detection processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
      

    # Find all the faces and face encodings in the current frame of video
    face_location = face_recognition.face_locations(small_frame, number_of_times_to_upsample=2)
    print(str(frames)+"-->"+str(face_location))
    
    if(temp==[]):
	   temp=face_location
	   for i in range(len(temp)):
	       p[i]=temp[i]
	       #print(str(frames)+"-->"+str(p))
	       os.system("mkdir ./register/P"+str(i))
    
    else:
        for j in face_location:
            for z in range(len(temp)):		
	            if(locations_compare(j,temp[z])==True):
	               #print(p)
                    	break
                    else:
	            	if(z<(len(temp)-1)):
	                   continue
	                else:
	                    if(len(os.listdir("./register"))==len(face_location)):
	                       break
	                    else:
                            	i=len(temp)
                            	p[i]=j
                            	#print(p)
                            	temp.append(j)
                            	os.system("mkdir ./register/P"+str(i))
					
	                                                                                                                                                                                                                                                  
    #print(str(frames)+"-->"+str(temp))
    for i,face in enumerate(face_location):
	
	

	offset=0.2
	height,width=frame.shape[0],frame.shape[1]
	print(height,width)
    	
	# Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top = face[0]*4
        right = face[1]*4
        bottom =face[2]*4
        left = face[3]*4
        
       	
	# Extract the region of the image that contains the face
        top,right,bottom,left=extend_boundaries(top,right,bottom,left,offset,height,width)
        face_image = frame[top:bottom,left:right]

        	# Blur the face image
        	#face_image = cv2.GaussianBlur(face_image, (99, 99), 30)

        	# Put the blurred face region back into the frame image
        	#frame[top:bottom, left:right] = face_image

        for j in range(len(temp)):
		#print("upload-->",temp)
		if (locations_compare(temp[j],face)==True):
        		out = cv2.imwrite('./register/P'+str(j)+'/frame%d.jpg'%frames, face_image)
    # Display the resulting image
    cv2.imshow('Video', frame)
    #count=0
    # Hit 'q' on the keyboard to quit!
    
    
	
    
	#count+=1
    frames = frames + 1
    if cv2.waitKey(1) and 0xFF == ord('q'):
	break
#end=time.time()
#print("time:",end-start)
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

#os.remove()
        
