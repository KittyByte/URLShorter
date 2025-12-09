from fastapi import HTTPException, status



credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
)

invalid_user_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

inactive_user_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, 
    detail='Inactive user'
)
