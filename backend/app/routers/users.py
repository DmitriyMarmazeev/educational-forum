from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas, auth
from app.models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=schemas.UserOut)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    # Получаем имя роли
    role_name = current_user.role.role_name
    user_out = schemas.UserOut(
        id_user=current_user.id_user,
        email=current_user.email,
        name=current_user.name,
        surname=current_user.surname,
        wallet=current_user.wallet,
        subscribed_until_date=current_user.subscribed_until_date,
        role_name=role_name
    )
    return user_out

@router.put("/me", response_model=schemas.UserOut)
async def update_me(
    user_update: schemas.UserUpdate,
    current_user: User = Depends(auth.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    updated_user = await crud.update_user(db, current_user, user_update)
    role_name =  updated_user.role.role_name
    return schemas.UserOut(
        id_user=updated_user.id_user,
        email=updated_user.email,
        name=updated_user.name,
        surname=updated_user.surname,
        wallet=updated_user.wallet,
        subscribed_until_date=updated_user.subscribed_until_date,
        role_name=role_name
    )

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: User = Depends(auth.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    await crud.soft_delete_user(db, current_user)
    return

@router.get("/{user_id}", response_model=schemas.UserProfileOut)
async def get_user_profile(
    user_id: int,
    current_user: User = Depends(auth.student_or_above),
    db: AsyncSession = Depends(get_db)
):
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    role_name = user.role.role_name
    return schemas.UserProfileOut(
        id_user=user.id_user,
        name=user.name if not user.is_deleted else "Удалённый",
        surname=user.surname if not user.is_deleted else "аккаунт",
        role_name=role_name,
        is_deleted=user.is_deleted
    )

@router.post("/apply-author", status_code=status.HTTP_200_OK)
async def apply_for_author(
    current_user: User = Depends(auth.student_or_above),
):
    # Заглушка
    return {"message": "Application submitted (stub)"}

@router.post("/subscribe", status_code=status.HTTP_200_OK)
async def subscribe(
    current_user: User = Depends(auth.student_or_above),
    db: AsyncSession = Depends(get_db)
):
    # Заглушка: продлеваем подписку на 30 дней
    from datetime import datetime, timedelta
    current_user.subscribed_until_date = datetime.utcnow() + timedelta(days=30)
    await db.commit()
    return {"message": "Subscription activated (stub)"}