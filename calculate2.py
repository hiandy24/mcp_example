# server.py
from fastmcp import FastMCP
import anyio

mcp = FastMCP("Demo 🚀")

@mcp.tool(name ="greet2", description="返回问候语: hello, {name}!")
async def greet(name: str) -> str:
    """返回问候语"""
    return f"hello, {name}!"

def add(a: int, b: int) -> int:
    """返回两个整数的和"""
    return a + b

mcp.tool(add, name ="add")

@mcp.resource("config://app", description="返回应用配置信息")
async def get_config() -> dict:
    """返回配置信息"""
    return '{debug: true, version: "1.0.0"}'

@mcp.resource("file://readme")
def get_readme() -> str:
    """返回README内容"""
    return "# Myapp \nThis is a demo application."

@mcp.resource("user://{user_id}/profile")
def get_user_profile(user_id: int) -> str:
    return f'{{"user_id": {user_id}, "name": "User{user_id}"}}' 



if __name__ == "__main__":
    # 使用无状态 HTTP，不需要会话管理
    mcp.run(transport="http", port=8000, stateless_http=True)