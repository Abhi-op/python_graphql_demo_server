import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey,DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api import db
    


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True, index=True)
    first_name = db.Column(String(255), nullable=True)
    last_name = db.Column(String(255), nullable=True)
    year_of_birth = db.Column(String(4), nullable=True)
    profile_pic_url = db.Column(String(2083), nullable=True)
    gender_id = db.Column(Integer, nullable=True)
    languages = db.Column(String(60), nullable=True)
    bio = db.Column(String(1024), nullable=True)
    created_at = db.Column(DateTime, nullable=True, server_default=text('now()'))
    updated_at = db.Column(DateTime, nullable=True, server_default=text('now()'))
    user_csv_uploads = db.relationship('UserCSVUploads', back_populates='users')
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "year_of_birth":self.year_of_birth,
            "profile_pic_url":self.profile_pic_url,
            "gender_id":self.gender_id,
            "languages":self.languages,
            "bio":self.bio,
            "created_at": str(self.created_at.strftime('%d-%m-%Y')),
            "updated_at": str(self.updated_at.strftime('%d-%m-%Y'))
        }

class UserCSVUploads(db.Model):
        __tablename__ = "UserCSVUploads"
        id = Column(Integer,primary_key = True,index = True)
        user_id = db.Column(Integer, db.ForeignKey("users.id"))
        csv_url = db.Column(String(512))
        users = db.relationship('Users', back_populates='user_csv_uploads')
        def to_dict(self):
             return {
                  "id":self.id,
                  "user_id":self.user_id,
                  "csv_url":self.csv_url
             }
        
class UserEmail(db.Model):
    __tablename__ = 'user_emails'

    id = Column(Integer, primary_key=True, autoincrement=True, name='pk_user_emails')
    user_id = Column(Integer, ForeignKey('users.id', name='user_emails_users_id_fk'), nullable=False)
    email = Column(String(128), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id', name='user_emails_ibfk_2'), nullable=False, default=9)
    created_ts = Column(DateTime, nullable=False, default=func.now())
    updated_ts = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_primary = Column(Boolean, nullable=False, default=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    fcm_key = Column(String(1024))
    fcm_apple_key = Column(String(1024))
    
    platforms = relationship('Platform', backref='user_emails', foreign_keys=[platform_id])
    users = relationship('User', backref='user_emails', foreign_keys=[user_id], cascade='all, delete-orphan')

class Platform(db.Model):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True, autoincrement=True, name='pk__platforms', server_default=text("nextval('_platforms_id_seq'::regclass)"))
    name = Column(String(64), unique=True, nullable=False, name='platforms__platforms')
    
   
    user_emails = relationship('UserEmail', backref='platforms')
    
    __table_args__ = {'schema': '_platforms'}

class ProfileHandles(db.Model):
    __tablename__ = 'profile_handles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    social_handle = Column(String(64), nullable=False)
    social_user_id = Column(String(128), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    is_private = Column(Boolean, default=False)
    total_posts = Column(Integer, default=0)
    profile_pic_url = Column(String(512))
    total_followers = Column(Integer, default=0)
    file_path = Column(String(512))
    access_token = Column(String(512))
    created_ts = Column(DateTime, nullable=False,  server_default=text('now()'))
    updated_ts = Column(DateTime, nullable=False,  server_default=text('now()'))

    platform = relationship("Platform", back_populates="profile_handles")
    profile = relationship("Profile", back_populates="profile_handles")

class Profiles(db.Model):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    display_name = Column(String(256), nullable=False)
    bio = Column(String(1024))
    custom_field_1 = Column(JSON)
    custom_field_2 = Column(JSON)
    custom_field_3 = Column(JSON)
    profile_pic_url = Column(String(512))
    is_hidden = Column(Boolean, default=False)
    optin_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    team_id = Column(Integer, nullable=False)
    is_master_profile = Column(Boolean, default=False)
    access_status_id = Column(Integer, ForeignKey('access_status.id'), default=1)
    viral_score = Column(Integer, default=0)
    contact_sms = Column(String(16))
    contact_email = Column(String(128))
    contact_chat = Column(String(128))
    owner_user_id = Column(Integer, nullable=False)
    admin_user_id = Column(Integer, nullable=False)
    created_by_user_id = Column(Integer, nullable=False)
    title_id = Column(Integer, ForeignKey('titles.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    profile_status_id = Column(Integer, ForeignKey('profile_statuses.id'))
    created_ts = Column(DateTime, nullable=False,  server_default=text('now()'))
    updated_ts = Column(DateTime, nullable=False,  server_default=text('now()'))

    access_status = relationship("AccessStatus", back_populates="profiles")
    titles = relationship("Titles", back_populates="profiles")
    users = relationship("Users", foreign_keys=[optin_user_id], backref="profiles")

class AccessStatus(db.Model):
    __tablename__ = "_access_status"

    id = Column(Integer, primary_key=True, server_default=text("nextval('_access_status_id_seq'::regclass)"))
    title = Column(String(16), nullable=False)
    profiles = relationship("Profile", back_populates="access_status")

    def __repr__(self):
        return f"<AccessStatus(id={self.id}, title={self.title})>"
class Titles(db.Model):
    __tablename__ = "_titles"

    id = Column(Integer, primary_key=True, server_default=text("nextval('_titles_id_seq'::regclass)"))
    title = Column(String(32))
    profiles = relationship("Profile", back_populates="titles")

    def __repr__(self):
        return f"<Titles(id={self.id}, title={self.title})>"