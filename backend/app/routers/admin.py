from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app import crud, schemas, auth
from app.models import User
from app.schemas import ChangeRoleRequest

router = APIRouter(prefix="/admin", tags=["Admin"])

# admin_only = auth.role_required(["admin"])

@router.get("/users", response_model=List[schemas.UserOut])
async def list_all_users(
    current_user: User =  Depends(auth.admin_or_above),
    db: AsyncSession = Depends(get_db)
):
    users = await crud.get_all_users_admin(db)
    result = []
    for u in users:
        role_name = u.role.role_name if u.role else "unknown"
        result.append(schemas.UserOut(
            id_user=u.id_user,
            email=u.email,
            name=u.name,
            surname=u.surname,
            role_name=role_name,
            is_deleted=u.is_deleted,
            subscribed_until_date=u.subscribed_until_date,
            wallet = u.wallet
        ))
    return result


@router.patch("/users/{user_id}/role", response_model=schemas.UserOut)
async def change_user_role(
    user_id: int,
    role_data: ChangeRoleRequest,
    current_user: User =  Depends(auth.admin_or_above),
    db: AsyncSession = Depends(get_db)
):
    # Нельзя менять роль самому себе (опционально)
    if user_id == current_user.id_user:
        raise HTTPException(status_code=400, detail="Cannot change your own role")
    updated_user = await crud.change_user_role(db, user_id, role_data.role_name)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User or role not found")
    await db.refresh(updated_user, attribute_names=['role'])
    role_name = updated_user.role.role_name
    return schemas.UserOut(
        id_user=updated_user.id_user,
        email=updated_user.email,
        name=updated_user.name,
        surname=updated_user.surname,
        role_name=role_name,
        is_deleted=updated_user.is_deleted,
        subscribed_until_date=updated_user.subscribed_until_date
    )