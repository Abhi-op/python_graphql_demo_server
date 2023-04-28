from .models import Users,UserCSVUploads
from api import db



def create_user_resolver(obj,info,first_name,last_name,year_of_birth,profile_pic_url,gender_id,languages,bio):
    try:
        user = Users(first_name=first_name,last_name=last_name,year_of_birth=year_of_birth,profile_pic_url = profile_pic_url,gender_id = gender_id,languages = languages,bio = bio)
        db.session.add(user)
        db.session.commit()
        payload = {
            "success":True,
            "message":str(user.to_dict())
        }
    except Exception as error:
           payload =  {
             "success":False,
             "message": "Error While creating the user"
            }
    return payload
def upload_csv_file(obj,info,userId,csv_file_url):
     try:
          file = UserCSVUploads(user_id = userId,csv_url = csv_file_url)
          db.session.add(file)
          db.session.commit()
          payload = {
               "success":True,
               "message":str(file.to_dict())
          }
     except Exception as error:
            payload = {
                 "success":False,
                 "message":"Error while uploading file url"
            } 
     return payload
          
def  delete_csv_file(obj,info,fileId):
      try:
           file = UserCSVUploads.query.get(fileId)

           if file:
            db.session.delete(file)
            db.session.commit()
            payload = {
                 "success":True,
                 "message":"file removed successfully"
            }
      except Exception as error:
              payload  = {
                   "success":False,
                   "message":"Error while deleting the file"
              }
      return payload
        

           