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