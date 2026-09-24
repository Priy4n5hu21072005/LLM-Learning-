from mcp.server import MCPServer
mcp=MCPServer("MCP_RESOURCE_PROMPTS")

@mcp.resource("project://file")
def project_info()->str:
    return """
Ai Code Review Agent

Purpose:
Review Github repository based on user-selected context.

Review Contexts:
-Security
-Performance
-Code Quality
-Architecture
-Bug detection
"""

@mcp.prompt()
def security_review()->str:
    return """
Review the provided code with a security-focused approach.

Check for:
-Authentication issues
-Hardcoded secrets
-Authorization issues
-Input Validation
-Injection vulnerabilities
-Unsafe data handling
"""

@mcp.tool()
def get_file_content(filename:str)->str:
    """Return the content of a project file."""
    file={
        "main.py":"print('hello world')",
        "auth.py":"def login():pass",
        "databases.py":"import psycog2"
    }
    if filename not in file:
        return f"file '{filename}' not found"
    return file[filename]

if __name__=="__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000 
    )