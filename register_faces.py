##########################################################################################
# Title         : Face registrer.
# Application   : Face Recognition
# Author        : Vrinda Prabhu
# Creation Date : 19/01/2018
# Description   : The register_face is responsible for updating the encodings database 
#                 of face recognition solution user. Currently works by running the code 
#                 giving the input as the folder containing minimum three photos of the
#                 person of interest.
#                   
#                 @TODO
#                 -> Make the registraction realtime
#                 -> Embeddings in a pickle file. Make a database for faster comparisions
#    
# Dependencies  : Ubuntu 14.04, python 2.7
##########################################################################################
import face_recognition
import os
import pickle
import glob

class Register(object):
    ###
    # The face registration class.
    #
    # The class generates the face encodings of the person who is registering and saves it in a encodings dictionary.
    # The key corresponds to the name of the person and value is a list of arrays with each array representing the encoding.
    #
    # NOTE : Minimum 3 photographs of the person is necessary for registration
    ###

    
    ENCODINGS_DICTIONARY = "encodings.pkl"
    REGISTER_FOLDER = "register"
    
    def __init__( self):
        '''
        The initialization function.

        Arguments -
            None
                               
        Return -
            None
            
        Creates or reads and encoding dictionary.The encoding dictionary which contains the key value pair of the 
        person and the encodings of person's photographs. 
        '''
        try:
            os.path.exists( self.ENCODINGS_DICTIONARY)
            with open( self.ENCODINGS_DICTIONARY, "r") as fp:
                self.encode_dict = pickle.load( fp)
        except:
            self.encode_dict = {}
        
        try:
            self.registrers = [x[0] for x in os.walk(self.REGISTER_FOLDER)][1:]
        except:
            print ("OK whom to register??")
	
	
            
        
    def create_encodings( self):
        '''
        Function to update/create the embeddings dictionary.
        
        Arguments -
            None
        
        Return -
            None
            
        @TODO 
        -> The name of the folder is taken as the register's name.
           Has to be made as a user input.
        -> Include checking for already available names in the dictionary
        '''
        for person in self.registrers:
            single_person = {}
            encodings = []
            image_files = []
            
            types = ('*.jpg', '*.png')
            for files in types:
                image_files.extend(glob.glob(os.path.join( person, files)))
            
            name = person.split("/")[-1]
            print "Encoding images for ", name
            
            for img in image_files:
                image = face_recognition.load_image_file(img)
		if (face_recognition.face_encodings(image))==[]:
			continue
                encodings.append(face_recognition.face_encodings(image)[0])
                
            single_person[name] = encodings
            
            self.encode_dict.update(single_person)
            
    
    def save_pickle( self):
        '''
        Function to save the enocings 
        
        Arguments -
            None
        
        Return -
            None
            
        @TODO 
        -> The name of the folder is taken as the register's name.
           Has to be made as a user input.
        -> Include checking for already available names in the dictionary
        '''
        with open( self.ENCODINGS_DICTIONARY,"w") as fp:
            pickle.dump(self.encode_dict, fp)
            
            
if __name__ == "__main__":
    register_obj = Register()
    register_obj.create_encodings()
    register_obj.save_pickle()
        
        
