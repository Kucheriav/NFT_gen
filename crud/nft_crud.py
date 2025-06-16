from models.nft_image import NFTImage
from sqlalchemy.orm import joinedload


def create_nft_image(session, user_id, filename, layers, title, layers_hash):
    nft = NFTImage(user_id=user_id, filename=filename, layers=layers, title=title, layers_hash=layers_hash)
    session.add(nft)
    session.commit()
    session.refresh(nft)
    return nft

def get_user_nft_images(session, user_id):
    return session.query(NFTImage).filter_by(user_id=user_id).all()

def get_nft_by_id(session, nft_id, user_id):
    return session.query(NFTImage).filter_by(id=nft_id, user_id=user_id).first()

def update_nft_title(session, nft_id, user_id, new_title):
    nft = get_nft_by_id(session, nft_id, user_id)
    if nft:
        nft.title = new_title
        session.commit()
        session.refresh(nft)
    return nft

def is_hash_exists(db, layers_hash):
    return db.query(NFTImage).filter(NFTImage.layers_hash == layers_hash).first() is not None

def get_all_nft_images_with_users(session):
    """
    Возвращает список объектов, в каждом из которых есть:
    - filename (имя файла)
    - title (пользовательское название)
    - created_at (дата создания)
    - layers (list)
    - username (имя пользователя-владельца)
    """
    # Предположим, что в NFTImage есть user_id, и у User есть username
    results = (
        session.query(NFTImage)
        .options(joinedload(NFTImage.user))  # подгружаем пользователя вместе с картинкой
        .order_by(NFTImage.created_at.desc())
        .all()
    )
    # Формируем удобный список для шаблона
    images = []
    for nft in results:
        images.append({
            "id": nft.id,
            "filename": nft.filename,
            "title": nft.title,
            "created_at": nft.created_at,
            "layers": nft.layers,
            "username": nft.user.username if nft.user else "Неизвестно"
        })
    return images