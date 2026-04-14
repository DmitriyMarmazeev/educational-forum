# @router.post("/tasks/{task_id}/rate", response_model=schemas.RatingOut)
# async def rate_task(
#     task_id: int,
#     rating_data: schemas.RatingCreate,
#     current_user: User = Depends(auth.student_or_above),
#     db: AsyncSession = Depends(get_db)
# ):
#     task = await crud.get_task_by_id(db, task_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     # Проверяем, не оценивал ли уже
#     existing = await crud.get_user_rating(db, task_id, current_user.id_user)
#     if existing:
#         # Обновляем оценку
#         rating = await crud.update_rating(db, existing.id_task_rating, rating_data.rating)
#     else:
#         rating = await crud.create_rating(db, task_id, current_user.id_user, rating_data.rating)
#     return schemas.RatingOut(
#         id_task_rating=rating.id_task_rating,
#         rating=rating.rating,
#         id_task=rating.id_task,
#         user_name=f"{current_user.name} {current_user.surname}"
#     )