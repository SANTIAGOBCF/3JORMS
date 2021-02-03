from app import db
from app import models

def get_user(user_alias):
    usr = models.User.query.filter_by(alias=user_alias).first()
    return usr

def get_post(user_alias):
    posts = models.Post.query.filter_by(author=get_user(user_alias))
    return posts

def get_post_list(user_alias):
    return get_post(user_alias).all()

def delete_all_post(user_alias):
    get_post(user_alias).delete()

def delete_user(user_alias):
    # secure erase user from db
    delete_all_post(user_alias)
    models.User.query.filter_by(alias=user_alias).delete()
