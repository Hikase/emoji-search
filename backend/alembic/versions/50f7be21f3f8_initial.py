"""initial

Revision ID: 50f7be21f3f8
Revises:
Create Date: 2025-01-30 14:31:11.236929

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "50f7be21f3f8"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "search_history",
        sa.Column("search_uid", sa.UUID(), nullable=False),
        sa.Column("query", sa.String(), nullable=False),
        sa.Column("duration", sa.Float(), nullable=False),
        sa.Column("result", sa.String(), nullable=False),
        sa.Column("searched_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("search_uid"),
    )
    op.create_table(
        "feedback",
        sa.Column("feedback_uid", sa.UUID(), nullable=False),
        sa.Column("search_uid", sa.UUID(), nullable=True),
        sa.Column("relevant_emoji", sa.String(), nullable=False),
        sa.Column("rationale", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["search_uid"],
            ["search_history.search_uid"],
        ),
        sa.PrimaryKeyConstraint("feedback_uid"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("feedback")
    op.drop_table("search_history")
    # ### end Alembic commands ###
