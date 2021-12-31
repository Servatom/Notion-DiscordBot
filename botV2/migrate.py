from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)