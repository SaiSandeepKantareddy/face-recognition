
import face_recognition
import cv2
import sys
import os
import pickle
import frames
import shutil

os.system('python register_faces.py')


class Recognize(object):
    '''
    This is a demo of running face recognition on live video from webcam. 
      1. Process each video frame at 1/4 resolution (though still display it at full resolution)
      2. Only detect faces in every other frame of video.
    '''
    
    ENCODINGS_DICTIONARY = "encodings.pkl"

    def __init__( self):
        '''
        The initialization function.

        Arguments -
            None
                               
        Return -
            None
            
        Loads the encodings dictionary which contains the key value pair of the 
        person and the encodings of person's photographs. 
        '''
        try:
            os.path.exists( self.ENCODINGS_DICTIONARY)
            with open( self.ENCODINGS_DICTIONARY, "r") as fp:
                self.encode_dict = pickle.load( fp)
        except:
            print "Error!! No one is registered!!"
            sys.exit(0)
        


    def _compare( self, in_face_encoding):
        '''
        Match the incoming face encoding with the saved face encodings.

        Arguments -
            in_face_encoding : The input face encoding

        Return -
            identity : The name of the person who closely matches the input face encoding

        @TODO
        -> Make the comparision faster using a different matching algorithm
        '''
        temp_name = "Unknown"
        for name, encoding_list in self.encode_dict.items():
            match = face_recognition.compare_faces( encoding_list, in_face_encoding, tolerance=0.5)
            #print match
            
            true_count = match.count(True)

            if true_count >= 5:
                temp_name = name
            
        return temp_name



    def recognize_faces( self):
        '''
        Method/Function to recognize face. Reads each frame of the video, encodes all the faces
        found in the frame, compare it with the existing encoding dictionary.

        If no name found annotates with unknown

        Arguments -
            None

        Return -
            None

        Returns the frame with annotated names on the faces.
        '''        

        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(-1)
	
        
	# Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True


        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                #print "Number of people", len(face_encodings)

                face_names = []
                for index_,face_encoding in enumerate(face_encodings):
                    # See if the face is a match for the known face(s)
                    #print "Face number --> ",index_
                    name = self._compare( face_encoding)
		   		
                    face_names.append(name)

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
		#if name!="Unknown":
                           
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
     		
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
	    #out1.write(frame)
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

	
        cv2.destroyAllWindows()


if __name__ == "__main__":
    recognizer_obj = Recognize()
    recognizer_obj.recognize_faces()
os.remove('./encodings.pkl')
for j in range(len(os.listdir("./register/"))):
	shutil.rmtree('./register/P'+str(j))
