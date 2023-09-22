from aiosqlite import connect

from config_data.config import load_config

config = load_config()


async def insert_data(table_name, column, values):
    async with connect(config.db.path) as db:
        query = f"INSERT INTO {table_name} ({column}) VALUES ({values}) ON CONFLICT DO NOTHING"
        await db.execute(query)
        await db.commit()


async def select_table(table_name):
    async with connect(config.db.path) as db:
        query = f"SELECT * FROM {table_name}"
        return await db.execute(query)


async def select_columns(table_name, columns):
    async with connect(config.db.path) as db:
        query = f"SELECT {columns} FROM {table_name}"
        return await db.execute(query)


async def select_data(table_name, condition):
    async with connect(config.db.path) as db:
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        return await db.execute(query)


async def select_columns_condition(table_name, columns, condition):
    async with connect(config.db.path) as db:
        query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
        return await db.execute(query)


async def select_exists(table_name, condition):
    async with connect(config.db.path) as db:
        query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {condition} LIMIT 1)"
        return await db.execute(query) == 1


async def delete_data(table_name, condition):
    async with connect(config.db.path) as db:
        query = f"DELETE FROM {table_name} WHERE {condition}"
        await db.execute(query)
        await db.commit()


async def update_data(table_name, set_values, condition):
    async with connect(config.db.path) as db:
        query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        await db.execute(query)
        await db.commit()
