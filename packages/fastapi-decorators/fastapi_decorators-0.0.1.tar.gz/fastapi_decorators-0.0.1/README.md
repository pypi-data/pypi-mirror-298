# FastAPI decorators

Small Python utility for wrapping your FastAPI endpoints in custom decorators.

## Installation
```bash
pip install fastapi-decorators
```

## Usage
Create a simple decorator that rejects unauthorized requests:

```python

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", 
    auto_error=False,
)

def authorize(*required_scopes: str):
    def decorator(func):
        def dependency(
            token: Optional[str] = Depends(oauth2_password_scheme),
            db_session: Session = Depends(get_db),
        ):
            if token is None:
                raise HTTPException(status_code=401, detail="Unauthenticated")

            jwt = decode_jwt(token)
            if not all(scope in jwt["scopes"] for scope in required_scopes):
                raise HTTPException(status_code=403, detail="Unauthorized")

            if not db_session.query(User).filter(User.id == jwt["sub"]).first():
                raise HTTPException(status_code=403, detail="Unauthorized")

        return add_dependencies(Depends(dependency))(func)
    return decorator
```

The decorator can be used like so:
```python
@app.put("/users/{user_id}")
@authorize("users:write")
def update_user(*, user_id: int, user_update: UserUpdate):
    ...
```
