from mcp.server.fastmcp import Context, FastMCP
from smithery.decorators import smithery


@smithery.server()
def create_server():
    """Create and return a FastMCP server instance."""
    
    mcp = FastMCP("Demo 🚀")

    @mcp.tool(name="greet2", description="返回问候语: hello, {name}!")
    async def greet(name: str, ctx: Context) -> str:
        """返回问候语"""
        return f"hello, {name}!"

    @mcp.tool(name="add", description="返回两个整数的和")
    def add(a: int, b: int, ctx: Context) -> int:
        """返回两个整数的和"""
        return a + b

    @mcp.resource("config://app", description="返回应用配置信息")
    async def get_config(ctx: Context) -> dict:
        """返回配置信息"""
        return {"debug": True, "version": "1.0.0"}

    @mcp.resource("file://readme", description="返回README内容")
    def get_readme(ctx: Context) -> str:
        """返回README内容"""
        return "# Myapp \nThis is a demo application."

    @mcp.resource("user://{user_id}/profile", description="返回用户配置文件")
    def get_user_profile(user_id: int, ctx: Context) -> dict:
        return {"user_id": user_id, "name": f"User{user_id}"}

    return mcp