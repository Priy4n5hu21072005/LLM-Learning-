from mcp.server import MCPServer
import requests

mcp=MCPServer("CodeReview")

@mcp.tool()
def get_github_repo(owner:str,repo:str)->dict:
    """Return basic information about a Github Repository"""

    url=f"https://api.github.com/repos/{owner}/{repo}"
    response=requests.get(url)
    if response.status_code !=200:
        return {
            "error":f"Github API returned {response.status_code}"
        }
    data=response.json()
    return {
        "name":data["name"],
        "full_name":data ["full_name"],
        "description":data["description"],
        "language":data["langugae"],
        "default_branch":data["default_branch"],
        "private":data["private"]
    }
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
        host="127.0.0.1",
        port=8000
    )