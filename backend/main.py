from typing import Union

from fastapi import FastAPI
import uvicorn
import psycopg2
import psycopg2.extras
import os

app = FastAPI()

class Database:
    def __init__(self) -> None:
        pass

    def findOneBy(self, criteria: dict = {}) -> dict:
        pass

    def findBy(self, criteria: dict) -> list:
        pass

class PostgresAdapter(Database):
    def __init__(self) -> None:
        Database.__init__(self)
        self.con = psycopg2.connect(
            database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'), host=os.getenv('POSTGRES_HOST'), port=os.getenv('POSTGRES_PORT'))
        self.cur = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS public.data(id SERIAL, type VARCHAR(255), url VARCHAR(255) NOT NULL, title VARCHAR(255) NOT NULL, price FLOAT NOT NULL, priceAfterDiscount FLOAT, created_at TIMESTAMP DEFAULT NOW(), modified_at TIMESTAMP DEFAULT NOW())")
        self.con.commit()

    def findOneBy(self, criteria: dict = {}) -> dict:
        criteria['limit'] = 1
        results = self.findBy(criteria)
        return results[0]

    def findBy(self, criteria: dict) -> list:
        limit = 20
        page = 1
        title = None

        if ('limit' in criteria and criteria['limit']):
            limit = criteria['limit']
            del criteria['limit']

        if ('page' in criteria and criteria['page']):
            page = criteria['page']
            del criteria['page']

        if ('title' in criteria and criteria['title']):
            title = criteria['title']
            del criteria['title']

        conditions = []
        params = []
        for key, value in criteria.items():
            conditions.append("{} = %s".format(key))
            params.append(value)

        if (title):
            conditions.append("LOWER(title) LIKE %s")
            params.append("%" + title + "%")

        query = "SELECT * FROM public.data "
        query += " WHERE " if bool(conditions) > 0 else ""
        query += " AND ".join(conditions)
        query += " LIMIT " + str(limit)
        query += " OFFSET " + str(limit * (page - 1))

        print(query, params)

        self.cur.execute(query, params)
        results = self.cur.fetchall()

        return results

@app.get("/api/latest")
async def latest():
    db = PostgresAdapter()

    return {
        'data': db.findOneBy()
    }

@app.get("/api/list")
async def list(limit: int = None, page: int = None, t: str = None, type: str = None):
    db = PostgresAdapter()

    criteria = {}

    if (limit):
        criteria['limit'] = limit

    if (page):
        criteria['page'] = page

    if (t):
        criteria['title'] = t.lower().strip()

    if (type and type in ['steam', 'gog']):
        criteria['type'] = type.lower().strip()

    return {
        'data': db.findBy(criteria)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
