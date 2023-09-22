import aiosqlite

from config_data.config import load_config

config = load_config()


class AsyncSQLiteDB:
    def __init__(self):
        self.db_name = config.db.path
        self.connection = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        self.connection = await aiosqlite.connect(self.db_name)

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def execute(self, query, parameters=None):
        async with self.connection.execute(query, parameters) as cursor:
            return await cursor.fetchall()

    async def commit(self):
        await self.connection.commit()

    async def insert_data(self, table_name, column, values):
        query = f"INSERT INTO {table_name} ({column}) VALUES ({values}) ON CONFLICT DO NOTHING"
        await self.execute(query)
        await self.commit()

    async def select_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        return await self.execute(query)

    async def select_data(self, table_name, condition):
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        return await self.execute(query)

    async def select_columns(self, table_name, columns):
        query = f"SELECT {columns} FROM {table_name}"
        return await self.execute(query)

    async def select_columns_condition(self, table_name, columns, condition):
        query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
        return await self.execute(query)

    async def select_exists(self, table_name, condition):
        query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {condition} LIMIT 1)"
        result = await self.execute(query)
        return result[0][0] == 1

    async def delete_data(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        await self.execute(query)
        await self.commit()

    async def update_data(self, table_name, set_values, condition):
        query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        await self.execute(query)
        await self.commit()


# Функция быстрого доступа к базе данных
async def insert_data(table_name, column, values):
    async with AsyncSQLiteDB() as db:
        await db.insert_data(table_name, column, values)
    return


async def select_table(table_name):
    async with AsyncSQLiteDB() as db:
        result = await db.select_table(table_name)
    return result


async def select_data(table_name, condition):
    async with AsyncSQLiteDB() as db:
        result = await db.select_data(table_name, condition)
    return result


async def select_columns(table_name, columns):
    async with AsyncSQLiteDB() as db:
        result = await db.select_columns(table_name, columns)
    return result


async def select_columns_condition(table_name, columns, condition):
    async with AsyncSQLiteDB() as db:
        result = await db.select_columns_condition(table_name, columns, condition)
    return result


async def select_exists(table_name, condition):
    async with AsyncSQLiteDB() as db:
        result = await db.select_exists(table_name, condition)
    return result


async def delete_data(table_name, condition):
    async with AsyncSQLiteDB() as db:
        await db.delete_data(table_name, condition)
    return


async def update_data(table_name, set_values, condition):
    async with AsyncSQLiteDB() as db:
        await db.update_data(table_name, set_values, condition)
    return
