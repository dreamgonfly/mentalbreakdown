from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
task = Table('task', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('raw', String(length=140)),
    Column('todo', String(length=100)),
    Column('estimated_time', Integer, default=ColumnDefault(1)),
    Column('due', DateTime),
    Column('completed', Boolean, default=ColumnDefault(False)),
    Column('completed_time', DateTime),
    Column('last_notnow', DateTime, default=ColumnDefault('0001-01-01 00:00:00')),
    Column('number_of_notnow', Integer, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['task'].columns['completed_time'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['task'].columns['completed_time'].drop()
