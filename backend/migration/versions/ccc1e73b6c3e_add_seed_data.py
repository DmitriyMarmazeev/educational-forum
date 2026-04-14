"""add_seed_data

Revision ID: ccc1e73b6c3e
Revises: 576a12376ccc
Create Date: 2026-04-14 19:38:08.712415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column


# revision identifiers, used by Alembic.
revision: str = 'ccc1e73b6c3e'
down_revision: Union[str, None] = '576a12376ccc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


roles_table = table(
    'roles',
    column('role_name', sa.String(50))
)

subjects_table = table(
    'subjects',
    column('subject_name', sa.String(100)),
    column('count_of_tasks', sa.Integer)
)

def upgrade():
    conn = op.get_bind()

    # === Роли ===
    # Проверяем, какие роли уже есть
    existing_roles = {row[0] for row in conn.execute(sa.text("SELECT role_name FROM roles")).fetchall()}
    needed_roles = ['admin', 'student', 'moderator', 'author']  # добавьте свои

    to_insert_roles = [{'role_name': r} for r in needed_roles if r not in existing_roles]
    if to_insert_roles:
        op.bulk_insert(roles_table, to_insert_roles)
        print(f"Inserted roles: {[r['role_name'] for r in to_insert_roles]}")
    else:
        print("All roles already exist, skipping")

    # === Предметы ===
    existing_subjects = {row[0] for row in conn.execute(sa.text("SELECT subject_name FROM subjects")).fetchall()}
    needed_subjects = [
        'Математика', 'Русский язык', 'Физика', 'Информатика', 'История'
    ]  # замените на свои

    to_insert_subjects = [
        {'subject_name': s, 'count_of_tasks': 0}
        for s in needed_subjects if s not in existing_subjects
    ]
    if to_insert_subjects:
        op.bulk_insert(subjects_table, to_insert_subjects)
        print(f"Inserted subjects: {[s['subject_name'] for s in to_insert_subjects]}")
    else:
        print("All subjects already exist, skipping")

def downgrade():
    # Откат: удаляем только те записи, которые могли быть добавлены этой миграцией.
    # Чтобы не задеть пользовательские данные, лучше ничего не делать.
    # Если очень нужно – раскомментируйте:
    # op.execute("DELETE FROM roles WHERE role_name IN ('admin', 'user', 'moderator')")
    # op.execute("DELETE FROM subjects WHERE subject_name IN ('Математика', 'Русский язык', 'Физика', 'Информатика', 'История')")
    pass