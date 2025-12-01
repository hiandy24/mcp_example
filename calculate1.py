import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 创建MCP服务器实例
app = Server("calculator-server")   

@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="calculate",
            description="执行基本的数学计算，支持加减乘除和括号",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，例如: '2 + 2', '(10 * 5) / 2', '3.14 * 2'"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="advanced_calculate",
            description="执行高级数学计算，支持幂运算、平方根、三角函数等",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，支持: ** (幂), sqrt(), sin(), cos(), tan(), log(), abs()"
                    }
                },
                "required": ["expression"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """处理工具调用"""
    
    if name == "calculate":
        expression = arguments.get("expression", "")
        try:
            # 安全地计算表达式（只允许基本运算）
            # 注意：使用eval有安全风险，这里仅用于演示
            # 生产环境应该使用更安全的解析器
            allowed_chars = set("0123456789+-*/(). ")
            if not all(c in allowed_chars for c in expression):
                return [TextContent(
                    type="text",
                    text=f"错误：表达式包含不允许的字符。只支持数字和 + - * / ( ) 运算符"
                )]
            
            result = eval(expression)
            return [TextContent(
                type="text",
                text=f"计算结果：{expression} = {result}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"计算错误：{str(e)}"
            )]
    
    elif name == "advanced_calculate":
        expression = arguments.get("expression", "")
        try:
            import math
            
            # 创建安全的命名空间，包含数学函数
            safe_dict = {
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'abs': abs,
                'pow': pow,
                'pi': math.pi,
                'e': math.e
            }
            
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return [TextContent(
                type="text",
                text=f"计算结果：{expression} = {result}"
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"计算错误：{str(e)}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"未知工具：{name}"
        )]

async def main():
    """主函数：启动stdio服务器"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    print("Starting Calculator MCP Server...")
    asyncio.run(main())