from database import SessionLocal, engine
import models


# get number of clients
def get_clients():
    db = SessionLocal()
    clients = db.query(models.Clients).all()
    return len(clients)
print(get_clients())