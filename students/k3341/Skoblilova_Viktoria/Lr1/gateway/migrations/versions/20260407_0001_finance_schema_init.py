"""initialize time-management schema

Revision ID: 20260407_0001
Revises:
Create Date: 2026-04-07 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260407_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("d_create", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("d_update", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.UniqueConstraint("email", name="uq_users_email"),
        schema="public",
    )

    op.create_table(
        "finance_accounts",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("color", sa.String(), nullable=False, server_default="blue"),
        sa.Column("priority_weight", sa.Float(), nullable=False, server_default="1"),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("d_create", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["public.users.id"], name="fk_finance_accounts_user_id"),
        sa.UniqueConstraint("user_id", "name", name="uq_finance_accounts_user_name"),
        schema="public",
    )

    op.create_table(
        "finance_categories",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("priority", sa.String(), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(), nullable=False, server_default="todo"),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("d_create", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["public.users.id"], name="fk_finance_categories_user_id"),
        sa.ForeignKeyConstraint(["account_id"], ["public.finance_accounts.id"], name="fk_finance_categories_account_id"),
        sa.UniqueConstraint("user_id", "name", "account_id", name="uq_finance_categories_user_name_account"),
        schema="public",
    )

    op.create_table(
        "finance_budgets",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("period", sa.String(), nullable=False, server_default="app"),
        sa.Column("period_start", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("remind_before_minutes", sa.Float(), nullable=False, server_default="30"),
        sa.Column("is_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("d_create", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["public.users.id"], name="fk_finance_budgets_user_id"),
        sa.ForeignKeyConstraint(["category_id"], ["public.finance_categories.id"], name="fk_finance_budgets_category_id"),
        sa.UniqueConstraint("user_id", "category_id", "period_start", name="uq_finance_budgets_user_category_period_start"),
        schema="public",
    )

    op.create_table(
        "finance_goals",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("date_for", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("planned_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="todo"),
        sa.Column("is_generated", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("d_create", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["public.users.id"], name="fk_finance_goals_user_id"),
        sa.UniqueConstraint("user_id", "name", name="uq_finance_goals_user_name"),
        schema="public",
    )

    op.create_table(
        "finance_transactions",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("spent_minutes", sa.Float(), nullable=False, server_default="0"),
        sa.Column("session_quality", sa.Float(), nullable=False, server_default="1"),
        sa.Column("note", sa.String(length=1024), nullable=True),
        sa.Column("happened_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("d_create", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["public.users.id"], name="fk_finance_transactions_user_id"),
        sa.ForeignKeyConstraint(["account_id"], ["public.finance_accounts.id"], name="fk_finance_transactions_account_id"),
        sa.ForeignKeyConstraint(["category_id"], ["public.finance_categories.id"], name="fk_finance_transactions_category_id"),
        schema="public",
    )

    op.create_table(
        "finance_tags",
        sa.Column("id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["public.users.id"], name="fk_finance_tags_user_id"),
        sa.UniqueConstraint("user_id", "name", name="uq_finance_tags_user_name"),
        schema="public",
    )

    op.create_table(
        "m2m_transaction_tags",
        sa.Column("transaction_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.Column("relevance_score", sa.Float(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(["transaction_id"], ["public.finance_transactions.id"], name="fk_m2m_transaction_tags_transaction_id"),
        sa.ForeignKeyConstraint(["tag_id"], ["public.finance_tags.id"], name="fk_m2m_transaction_tags_tag_id"),
        sa.PrimaryKeyConstraint("transaction_id", "tag_id", name="pk_m2m_transaction_tags"),
        sa.UniqueConstraint("transaction_id", "tag_id", name="uq_m2m_transaction_tags_transaction_tag"),
        schema="public",
    )


def downgrade() -> None:
    op.drop_table("m2m_transaction_tags", schema="public")
    op.drop_table("finance_tags", schema="public")
    op.drop_table("finance_transactions", schema="public")
    op.drop_table("finance_goals", schema="public")
    op.drop_table("finance_budgets", schema="public")
    op.drop_table("finance_categories", schema="public")
    op.drop_table("finance_accounts", schema="public")
    op.drop_table("users", schema="public")
