from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'g7a8b9c0d1e2'
down_revision: Union[str, Sequence[str], None] = 'f6a7b8c9d0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'knowledge_documents',
        sa.Column('source_content', sa.LargeBinary(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('knowledge_documents', 'source_content')
