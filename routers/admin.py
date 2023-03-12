from fastapi import APIRouter, status, Depends
from Database.database import session, engine
from schemas import SignUpModel
from Database.models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from schemas import LoginModel

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

session=session(bind=engine)

@auth_router.get('/')
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token.")
    return {'message': 'Hello World'}

@auth_router.post(
        '/signup', 
        status_code=status.HTTP_201_CREATED
        )
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail= "User email is already in use.")
    
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail= "User email is already in use.")
    
    new_user = User(
        username=user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_admin = user.is_admin
    )

    session.add(new_user)
    session.commit()

    return new_user


#login route

@auth_router.post('/login', status_code = 200)
async def login(user: LoginModel, Authorize: AuthJWT=Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token
        } 
        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail = "Invalid username or password")


# Refreshing tokens
@auth_router.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please provide valid refresh token")
    
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access_token", access_token})