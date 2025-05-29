from models.user import User

def get_user_by_username(session, username):
    return session.query(User).filter_by(username=username).first()

def create_user(session, username, password_hash):
    user = User(username=username, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_id(session, user_id):
    return session.query(User).filter_by(id=user_id).first()