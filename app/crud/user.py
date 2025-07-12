from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    """
    Obtém um usuário do banco de dados pelo ID.

    Args:
        db (Session): A sessão do banco de dados.
        user_id (int): O ID do usuário a ser recuperado.

    Returns:
        User: O objeto User se encontrado, caso contrário, None.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    Obtém um usuário do banco de dados pelo endereço de e-mail.

    Args:
        db (Session): A sessão do banco de dados.
        email (str): O endereço de e-mail do usuário a ser recuperado.

    Returns:
        User: O objeto User se encontrado, caso contrário, None.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    """
    Cria um novo usuário no banco de dados.

    Args:
        db (Session): A sessão do banco de dados.
        user (UserCreate): O objeto UserCreate contendo os dados do novo usuário.

    Returns:
        User: O objeto User recém-criado.
    """
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
