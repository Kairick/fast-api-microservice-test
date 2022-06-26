from fastapi import HTTPException


async def validate_token_data(data: dict) -> None:
    """Проверяет валидность данных токена"""
    if data['expired']:
        raise HTTPException(status_code=401,
                            detail='Token is expired. Refresh your token')
    if not data['success']:
        raise HTTPException(status_code=401,
                            detail='Token is not valid.')
