import os
import asyncio
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp import types
import psycopg2
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection settings
DB_CONFIG = {
    'host': 'localhost',
    'database': 'vikings_analytics',
    'user': 'postgres',
    'password': os.environ.get('POSTGRES_PASSWORD')
}

# Create MCP server instance
server = Server("vikings-analytics-mcp")

def get_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(**DB_CONFIG)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool defines a function Claude can call.
    """
    return [
        types.Tool(
            name="query_vikings_data",
            description="Execute SQL queries against the Vikings database. Available tables: 'plays' (play-by-play 1999-2025), 'moss_1998_games' (Randy Moss's 1998 rookie season game stats), and views (fourth_down_plays, red_zone_plays, vikings_offense).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute against vikings_analytics database"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict
) -> list[types.TextContent]:
    """
    Handle tool execution.
    This runs when Claude calls one of the tools.
    """
    if name != "query_vikings_data":
        raise ValueError(f"Unknown tool: {name}")

    query = arguments.get("query")
    if not query:
        raise ValueError("Missing query parameter")

    try:
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute query
        cursor.execute(query)

        # Fetch results
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description] if cursor.description else []

        # Close connection
        cursor.close()
        conn.close()

        # Format results as JSON
        formatted_results = [
            dict(zip(column_names, row))
            for row in results
        ]

        return [
            types.TextContent(
                type="text",
                text=json.dumps(formatted_results, indent=2, default=str)
            )
        ]

    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"Error executing query: {str(e)}"
            )
        ]

async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="vikings-analytics-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
