"""3.10.1

Revision ID: 7d00e96862ae
Revises: 8894f8ca4aa4
Create Date: 2025-06-20 16:27:42.164138

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d00e96862ae'
down_revision = '8894f8ca4aa4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vadmin_resource_images')
    op.alter_column('vadmin_auth_dept', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_dept', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_menu', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_menu', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_role', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_role', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_user', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_user', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue_category', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue_category', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_login', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_login', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_sms_send', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_sms_send', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_details', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_details', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_type', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_type', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings_tab', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings_tab', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_comment='更新时间',
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vadmin_system_settings_tab', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings_tab', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_settings', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_type', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_type', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_details', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_system_dict_details', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_sms_send', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_sms_send', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_login', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_record_login', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue_category', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue_category', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_help_issue', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_user', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_user', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_role', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_role', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_menu', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_menu', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_dept', 'update_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='更新时间',
               existing_nullable=False)
    op.alter_column('vadmin_auth_dept', 'create_datetime',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_comment='创建时间',
               existing_nullable=False)
    op.create_table('vadmin_resource_images',
    sa.Column('filename', mysql.VARCHAR(length=255), nullable=False, comment='原图片名称'),
    sa.Column('image_url', mysql.VARCHAR(length=500), nullable=False, comment='图片链接'),
    sa.Column('create_user_id', mysql.INTEGER(), autoincrement=False, nullable=False, comment='创建人'),
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False, comment='主键ID'),
    sa.Column('create_datetime', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'),
    sa.Column('update_datetime', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='更新时间'),
    sa.Column('delete_datetime', mysql.DATETIME(), nullable=True, comment='删除时间'),
    sa.Column('is_delete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False, comment='是否软删除'),
    sa.ForeignKeyConstraint(['create_user_id'], ['vadmin_auth_user.id'], name='vadmin_resource_images_ibfk_1', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    comment='图片素材表',
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_comment='图片素材表',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
