from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from pydantic import BaseModel

# Configuração do banco de dados SQLite e SQLAlchemy
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Modelo de Usuário
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


# Definir o schema para a criação do usuário
class UserCreate(BaseModel):
    username: str
    password: str


# Definir o schema para o login
class LoginData(BaseModel):
    username: str
    password: str


Base.metadata.create_all(bind=engine)

# Configuração de Criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


# Função para obter o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Função para verificar senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Função para criar senha hash
def get_password_hash(password):
    return pwd_context.hash(password)


# Função de autenticação do usuário
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


# Rota para criar usuário (para fins de teste)
@app.post("/create-user/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Verificar se o usuário já existe
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Usuário já existe.")

        # Criar um novo usuário
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"msg": "Usuário criado com sucesso!"}

    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        raise HTTPException(
            status_code=500, detail=f"Erro ao criar o usuário: {str(e)}"
        )


# Rota de login
@app.post("/login/")
def login(login_data: LoginData, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )
    return {"msg": "Login realizado com sucesso!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
