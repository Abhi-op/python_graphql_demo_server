from .models import Users,UserCSVUploads
from api import db


def get_all_users_resolver(obj, info):
    try:
        users = [user.to_dict() for user in Users.query.all()]  
        payload = {  
            "success": True,
            "users": users  
        }
        return users
    except Exception as error:
        payload = { 
            "success": False,
            "errors": [str(error)]
        }
        return "Error"
def get_user_by_id(obj,info,userId):
    try:
        user = Users.query.get(userId)
        return user
    except Exception as error:
        return "Error"
def get_all_csv_files(obj, info, userId):
     try: 
          user = Users.query.get(userId)

          if user:
                  files = UserCSVUploads.query.filter_by(user_id=userId).all()
                  return files
          
     except Exception as error:
               payload  = {
                  "success":False,
                  "error":[str(error)]
               }
               return payload
