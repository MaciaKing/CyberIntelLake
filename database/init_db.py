from database.database import Base, engine
from models.file_progress import FileProgress
from models.batch_progres import LastBatchNumber

# Crear todas las tablas
Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente")