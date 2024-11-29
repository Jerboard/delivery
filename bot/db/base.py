import typing as t
import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncConnection

from init import ENGINE

METADATA = sa.MetaData ()


def begin_connection() -> t.AsyncContextManager [AsyncConnection]:
    ENGINE.connect ()
    return ENGINE.begin ()


async def init_models():
    async with ENGINE.begin () as conn:
        await conn.run_sync (METADATA.create_all)


# async def syncing_id():
#     with begin_connection () as conn:
#         await conn.execute (sa.text ("SELECT setval('orders_ggl_id_seq', (SELECT MAX(id) FROM orders_ggl));"))


# создать колонку
# with begin_connection() as conn:
#     # Добавляем новую колонку к таблице
#     conn.execute(sa.text('ALTER TABLE my_table ADD COLUMN comp_opr VARCHAR'))


async def create_trigger():
    async with ENGINE.begin() as conn:
        # Выполнить команду создания функции
        # await conn.execute(sa.text("""
        #     CREATE OR REPLACE FUNCTION update_orders_ggl_id()
        #     RETURNS TRIGGER AS $$
        #     BEGIN
        #         NEW.id := (SELECT COALESCE(MAX(id), 0) + 1 FROM orders_ggl);
        #         RETURN NEW;
        #     END;
        #     $$ LANGUAGE plpgsql;
        # """))

        await conn.execute(sa.text("""
            CREATE OR REPLACE FUNCTION update_orders_ggl_id()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.id IS NULL THEN
                    NEW.id := (SELECT COALESCE(MAX(id), 0) + 1 FROM orders_ggl);
                END IF;
                RETURN NEW;
             END;
            $$ LANGUAGE plpgsql;
        """))

        # Выполнить команду создания триггера, если он не существует
        await conn.execute(sa.text("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM pg_trigger
                    WHERE tgname = 'orders_ggl_id_trigger'
                ) THEN
                    CREATE TRIGGER orders_ggl_id_trigger
                    BEFORE INSERT ON orders_ggl
                    FOR EACH ROW
                    EXECUTE FUNCTION update_orders_ggl_id();
                END IF;
            END $$;
        """))

'''
CREATE OR REPLACE FUNCTION update_orders_ggl_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.id IS NULL THEN
        NEW.id := (SELECT COALESCE(MAX(id), 0) + 1 FROM orders_ggl);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
'''
