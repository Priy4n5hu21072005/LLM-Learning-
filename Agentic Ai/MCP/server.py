from mcp.server import MCPServer

mcp=MCPServer("CodeReview")

@mcp.tool()
def get_file_content(filename:str)->str:
    """Return the content of a project file."""
    files={
        "main.py": "print('Hello World')",
        "auth.py": "def login(): pass",
        "database.py": "import psycopg2"
    }

    if filename not in files:
        return f"File '{filename}' not found"

    return files[filename]
@mcp.tool()
def search_file(filename: str, keyword: str) -> str:
    """Search for a keyword inside a project file."""

    files = {
        "main.py": "print('Hello World')\nprint('Python')",
        "auth.py": "def login(): pass\ndef logout(): pass",
        "database.py": "import psycopg2\nconnect_database()"
    }

    if filename not in files:
        return f"File '{filename}' not found"

    content = files[filename]

    if keyword in content:
        return f"'{keyword}' found in {filename}"

    return f"'{keyword}' not found in {filename}"


@mcp.tool()
def list_project_files() -> list[str]:
    """Return the files available in the project."""

    return [
        "main.py",
        "auth.py",
        "database.py",
        "requirements.txt"
    ]

if __name__=="__main__":
    mcp.run(
        transport="streamable-http",
        port=8000,
        host="127.0.0.1"
    )