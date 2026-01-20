#!/usr/bin/env python3
"""
Test script to verify database connection is properly configured
"""

import asyncio
from src.hackathon_todo_api.database import async_engine
from sqlmodel import SQLModel
from sqlalchemy import text

async def test_connection():
    """Test the async database connection"""
    try:
        # Try to connect and run a simple query
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✓ Async database connection successful!")

            # Check if the SQLModel metadata is properly configured
            print(f"✓ SQLModel metadata contains {len(SQLModel.metadata.tables)} tables")
            for table_name in SQLModel.metadata.tables.keys():
                print(f"  - {table_name}")

    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

    return True

if __name__ == "__main__":
    print("Testing database connection...")
    success = asyncio.run(test_connection())

    if success:
        print("\n✓ Database connection test passed!")
    else:
        print("\n✗ Database connection test failed!")