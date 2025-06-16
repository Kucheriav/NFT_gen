import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from models.user import User
from models.nft_image import NFTImage
from database import SessionLocal
from models.nft_image import NFTImage
from services.nft_generator import get_layers_hash

db = SessionLocal()
for nft in db.query(NFTImage).filter(NFTImage.layers_hash == None):
    layers = nft.layers  # предполагается, что это dict/list
    nft.layers_hash = get_layers_hash(layers)
    db.add(nft)
db.commit()
db.close()