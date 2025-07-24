# Hello World MCP Server

A simple **Model Context Protocol (MCP)** server implementation in Python, designed as a learning template for developers who want to understand how to build MCP servers.

## What is MCP?

The Model Context Protocol (MCP) is a standardized protocol for connecting AI assistants (like Claude) with external tools, resources, and data sources. This Hello World server demonstrates the three core MCP concepts:

- **Tools**: Functions that can be called by the AI assistant
- **Resources**: Data that can be read by the AI assistant  
- **Prompts**: Templates that can be used to generate responses

## Features

This server implements:

### 🛠️ Tools
- `hello_world()` - Returns a simple greeting message
- `get_current_time()` - Provides current date and time with timezone info
- `echo(message)` - Echoes back your message with additional formatting

### 📚 Resources  
- `server://info` - JSON containing server metadata and capabilities

### 💬 Prompts
- `greeting` - Multi-language greeting template (English, German, Spanish)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone this repository**
   ```bash
   git clone https://github.com/raifdmueller/hello-world-mcp-python.git
   cd hello-world-mcp-python
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the server** (optional)
   ```bash
   python main.py
   ```
   The server should start and show initialization messages in stderr.

## Claude Desktop Integration

To use this MCP server with Claude Desktop:

### 1. Update Claude Desktop Configuration

Edit your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the server configuration:

```json
{
  "mcpServers": {
    "hello-world-python": {
      "command": "python",
      "args": ["/absolute/path/to/hello-world-mcp-python/main.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/hello-world-mcp-python"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/hello-world-mcp-python/` with the actual absolute path to your project directory.

### 2. Restart Claude Desktop

Close and restart Claude Desktop for the configuration to take effect.

### 3. Verify Connection

In Claude Desktop, you should see:
- The server appears in the MCP connection status
- You can call tools like `hello_world`, `get_current_time`, and `echo`
- You can access the `server://info` resource
- You can use the `greeting` prompt

## Usage Examples

Once connected to Claude Desktop, you can:

### Use Tools
```
Can you call the hello_world tool?
Can you get the current time?
Can you echo back "Hello MCP!"?
```

### Access Resources
```
Can you read the server info resource?
What capabilities does this server have?
```

### Generate Prompts
```
Can you generate a greeting prompt in German?
Show me the greeting prompt in Spanish?
```

## Project Structure

```
hello-world-mcp-python/
├── main.py                      # Main server implementation
├── requirements.txt             # Python dependencies
├── README.md                   # This documentation
├── claude_desktop_config.json  # Example Claude Desktop config
└── .gitignore                  # Git ignore rules
```

## Code Architecture

The server is organized into logical sections:

1. **Server Initialization** - Setup and metadata
2. **Tool Implementations** - The three demo tools
3. **Resource Implementations** - Server info resource
4. **Prompt Implementations** - Multi-language greeting
5. **Server Lifecycle** - Initialization and cleanup
6. **Main Loop** - stdio transport and error handling

## Development

### Adding New Tools

To add a new tool, use the `@server.call_tool()` decorator:

```python
@server.call_tool()
async def my_new_tool(param1: str, param2: int) -> List[types.TextContent]:
    """Tool description for documentation."""
    try:
        # Your tool logic here
        result = f"Processed {param1} with {param2}"
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        error_msg = f"Error in my_new_tool: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]
```

### Adding New Resources

1. Update `handle_list_resources()` to include your resource
2. Update `handle_read_resource()` to handle your resource URI

### Adding New Prompts

1. Update `handle_list_prompts()` to include your prompt
2. Update `handle_get_prompt()` to generate your prompt

## Troubleshooting

### Server Won't Start
- Check Python version: `python --version` (needs 3.8+)
- Verify dependencies: `pip install -r requirements.txt`
- Check file permissions: `chmod +x main.py`

### Claude Desktop Won't Connect
- Verify absolute paths in configuration
- Check Claude Desktop logs for error messages
- Ensure server starts successfully when run manually
- Restart Claude Desktop after configuration changes

### Tools Not Working
- Check server logs in stderr
- Verify tool parameters match expected types
- Test tools individually by calling them in Claude

## Learning Resources

To learn more about MCP:
- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

## License

MIT License - Feel free to use this as a template for your own MCP servers!

## Contributing

This is a learning template. Feel free to:
- Fork and modify for your needs
- Submit improvements via pull requests
- Share your own MCP server implementations

## Support

If you run into issues:
1. Check this README thoroughly
2. Review the code comments in `main.py`
3. Test the server manually outside of Claude Desktop
4. Check Claude Desktop configuration and logs

Happy MCP server building! 🚀
