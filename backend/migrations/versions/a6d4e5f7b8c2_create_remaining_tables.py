"""create remaining tables

Revision ID: a6d4e5f7b8c2
Revises: 5ed15047886b
Create Date: 2026-07-11 17:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a6d4e5f7b8c2'
down_revision: Union[str, Sequence[str], None] = '5ed15047886b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Events Table
    op.create_table(
        'events',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('client', sa.String(length=100), nullable=False),
        sa.Column('event_date', sa.Date(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('cover_image_id', sa.Uuid(), nullable=True),
        sa.Column('gallery_image_ids', sa.ARRAY(sa.Uuid()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['cover_image_id'], ['uploads.id'], name=op.f('fk_events_cover_image_id_uploads')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_events'))
    )
    op.create_index(op.f('ix_events_is_active'), 'events', ['is_active'], unique=False)
    op.create_index(op.f('ix_events_is_featured'), 'events', ['is_featured'], unique=False)
    op.create_index(op.f('ix_events_display_order'), 'events', ['display_order'], unique=False)

    # 2. Testimonials Table
    op.create_table(
        'testimonials',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('company', sa.String(length=100), nullable=True),
        sa.Column('testimonial', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('photo_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['photo_id'], ['uploads.id'], name=op.f('fk_testimonials_photo_id_uploads')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_testimonials'))
    )
    op.create_index(op.f('ix_testimonials_is_active'), 'testimonials', ['is_active'], unique=False)
    op.create_index(op.f('ix_testimonials_display_order'), 'testimonials', ['display_order'], unique=False)

    # 3. FAQs Table
    op.create_table(
        'faqs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('question', sa.String(length=300), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_faqs'))
    )
    op.create_index(op.f('ix_faqs_is_active'), 'faqs', ['is_active'], unique=False)
    op.create_index(op.f('ix_faqs_display_order'), 'faqs', ['display_order'], unique=False)

    # 4. Contact Messages Table
    op.create_table(
        'contact_messages',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=30), nullable=True),
        sa.Column('subject', sa.String(length=200), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_contact_messages'))
    )
    op.create_index(op.f('ix_contact_messages_is_read'), 'contact_messages', ['is_read'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_contact_messages_is_read'), table_name='contact_messages')
    op.drop_table('contact_messages')
    op.drop_index(op.f('ix_faqs_display_order'), table_name='faqs')
    op.drop_index(op.f('ix_faqs_is_active'), table_name='faqs')
    op.drop_table('faqs')
    op.drop_index(op.f('ix_testimonials_display_order'), table_name='testimonials')
    op.drop_index(op.f('ix_testimonials_is_active'), table_name='testimonials')
    op.drop_table('testimonials')
    op.drop_index(op.f('ix_events_display_order'), table_name='events')
    op.drop_index(op.f('ix_events_is_featured'), table_name='events')
    op.drop_index(op.f('ix_events_is_active'), table_name='events')
    op.drop_table('events')
