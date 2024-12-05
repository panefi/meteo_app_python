import os
import aiomysql
from dotenv import load_dotenv 

load_dotenv()

class SQLConnection:
    def __init__(self):
        """Connects to the database"""
        self.mydb = None
        self.mycursor = None

    async def __aenter__(self):
        """Establish the database connection"""
        self.mydb = await aiomysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT")),
            db=os.getenv("DB_NAME")
        )
        self.mycursor = await self.mydb.cursor(aiomysql.DictCursor)  # Use a dictionary cursor
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection"""
        if exc_type is None:
            await self.mydb.commit()
        else:
            await self.mydb.rollback()
        if self.mycursor:
            await self.mycursor.close()
        if self.mydb:
            self.mydb.close()

    async def execute_query(self, query, params=None):
        """Executes a query and returns the result"""
        await self.mycursor.execute(query, params)
        return await self.mycursor.fetchall()
