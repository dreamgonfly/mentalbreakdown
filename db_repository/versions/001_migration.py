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
    Column('last_notnow', DateTime),
    Column('number_of_notnow', Integer, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['task'].columns['last_notnow'].create()
    post_meta.tables['task'].columns['number_of_notnow'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['task'].columns['last_notnow'].drop()
    post_meta.tables['task'].columns['number_of_notnow'].drop()
