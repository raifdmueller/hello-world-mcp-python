#!/usr/bin/env python3
"""
Hello World MCP Server

A simple Model Context Protocol (MCP) server implementation that demonstrates
the basic concepts: Tools, Resources, and Prompts.

This server is designed as a learning template for developers who want to 
understand how to build MCP servers in Python.

Author: Claude (Anthropic)
Version: 1.0.0
License: MIT
"""

import asyncio
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# Import MCP library components
from mcp import Server, types
from mcp.server import NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio


# =============================================================================
# 1. SERVER INITIALIZATION AND METADATA
# =============================================================================

# Create the MCP server instance
server = Server("hello-world-mcp")

# Server metadata for identification
SERVER_INFO = {
    "name": "Hello World MCP Server", 
    "version": "1.0.0",
    "description": "A simple MCP server for learning purposes",
    "features": ["tools", "resources", "prompts"],
    "tools_count": 3,
    "created": datetime.now(timezone.utc).isoformat()
}

# Multi-language greeting templates
GREETING_TEMPLATES = {
    "en": """Hello! I'm a friendly MCP server built for learning purposes. 
I can help you understand how MCP servers work by demonstrating:
- Tools: Functions you can call (like getting the time)
- Resources: Data I can provide (like server information) 
- Prompts: Templates I can generate (like this greeting)

Try calling my tools or asking for my resources!""",
    
    "de": """Hallo! Ich bin ein freundlicher MCP Server, der zu Lernzwecken erstellt wurde.
Ich kann dir helfen zu verstehen, wie MCP Server funktionieren, indem ich demonstriere:
- Tools: Funktionen, die du aufrufen kannst (wie die Uhrzeit abfragen)
- Resources: Daten, die ich bereitstellen kann (wie Server-Informationen)
- Prompts: Vorlagen, die ich generieren kann (wie diese Begrüßung)

Probiere meine Tools aus oder frage nach meinen Ressourcen!""",
    
    "es": """¡Hola! Soy un servidor MCP amigable creado con fines de aprendizaje.
Puedo ayudarte a entender cómo funcionan los servidores MCP demostrando:
- Tools: Funciones que puedes llamar (como obtener la hora)
- Resources: Datos que puedo proporcionar (como información del servidor)
- Prompts: Plantillas que puedo generar (como este saludo)

¡Prueba mis herramientas o pregunta por mis recursos!"""
}


# =============================================================================
# 2. TOOL IMPLEMENTATIONS  
# =============================================================================

@server.call_tool()
async def hello_world() -> List[types.TextContent]:
    """
    Simple hello world tool that returns a greeting message.
    
    This is the most basic MCP tool - it takes no parameters and returns
    a simple text response.
    
    Returns:
        List[types.TextContent]: A greeting message
    """
    try:
        message = "Hello, World from MCP! 🌍 This is your first MCP server response."
        return [types.TextContent(type="text", text=message)]
    except Exception as e:
        error_msg = f"Error in hello_world tool: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]


@server.call_tool()
async def get_current_time() -> List[types.TextContent]:
    """
    Tool that returns the current date and time with timezone information.
    
    Demonstrates working with Python's datetime module and formatting
    output for human readability.
    
    Returns:
        List[types.TextContent]: Current time with timezone info
    """
    try:
        now = datetime.now(timezone.utc)
        local_time = now.astimezone()
        
        formatted_time = {
            "utc_time": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "local_time": local_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "iso_format": now.isoformat(),
            "timestamp": now.timestamp()
        }
        
        response = f"""Current Time Information:
🕐 UTC Time: {formatted_time['utc_time']}
🏠 Local Time: {formatted_time['local_time']}
📅 ISO Format: {formatted_time['iso_format']}
⏱️  Timestamp: {formatted_time['timestamp']}"""
        
        return [types.TextContent(type="text", text=response)]
    except Exception as e:
        error_msg = f"Error getting current time: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]


@server.call_tool()
async def echo(message: str) -> List[types.TextContent]:
    """
    Echo tool that repeats back the provided message with some formatting.
    
    Demonstrates parameter handling and input validation in MCP tools.
    
    Args:
        message: The text message to echo back
        
    Returns:
        List[types.TextContent]: The echoed message with formatting
    """
    try:
        # Input validation
        if not message:
            return [types.TextContent(
                type="text", 
                text="Error: No message provided to echo. Please provide a message parameter."
            )]
        
        if len(message) > 1000:
            return [types.TextContent(
                type="text",
                text="Error: Message too long. Please provide a message under 1000 characters."
            )]
        
        # Echo the message with formatting
        response = f"""Echo Response:
📝 Original: "{message}"
📏 Length: {len(message)} characters
🔄 Reversed: "{message[::-1]}"
📊 Word Count: {len(message.split())} words"""
        
        return [types.TextContent(type="text", text=response)]
    except Exception as e:
        error_msg = f"Error in echo tool: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]


# =============================================================================
# 3. RESOURCE IMPLEMENTATIONS
# =============================================================================

@server.list_resources()
async def handle_list_resources() -> List[types.Resource]:
    """
    List all available resources that this server provides.
    
    Resources are pieces of data that the server can provide, like files,
    API responses, or computed information.
    
    Returns:
        List[types.Resource]: List of available resources
    """
    return [
        types.Resource(
            uri="server://info",
            name="Server Information",
            description="Detailed information about this MCP server including capabilities and metadata",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """
    Read and return the content of a specific resource.
    
    Args:
        uri: The URI of the resource to read
        
    Returns:
        str: The resource content (JSON formatted for server info)
        
    Raises:
        ValueError: If the requested resource URI is not found
    """
    if uri == "server://info":
        # Return server information as JSON
        server_info = SERVER_INFO.copy()
        # Add current timestamp for when info was requested
        server_info["info_requested_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(server_info, indent=2)
    else:
        raise ValueError(f"Unknown resource URI: {uri}")


# =============================================================================
# 4. PROMPT IMPLEMENTATIONS
# =============================================================================

@server.list_prompts()
async def handle_list_prompts() -> List[types.Prompt]:
    """
    List all available prompts that this server can generate.
    
    Prompts are templates that can be used to generate text for various
    purposes, potentially with parameters.
    
    Returns:
        List[types.Prompt]: List of available prompts
    """
    return [
        types.Prompt(
            name="greeting",
            description="Generate a friendly greeting message in multiple languages",
            arguments=[
                types.PromptArgument(
                    name="language",
                    description="Language code for the greeting (en, de, es)",
                    required=False
                )
            ]
        )
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: Optional[Dict[str, str]]) -> types.GetPromptResult:
    """
    Generate a specific prompt with the given parameters.
    
    Args:
        name: The name of the prompt to generate
        arguments: Optional dictionary of arguments for the prompt
        
    Returns:
        types.GetPromptResult: The generated prompt content
        
    Raises:
        ValueError: If the prompt name is not recognized
    """
    if name == "greeting":
        # Get language from arguments, default to English
        language = "en"
        if arguments and "language" in arguments:
            requested_lang = arguments["language"].lower()
            if requested_lang in GREETING_TEMPLATES:
                language = requested_lang
        
        # Get the appropriate greeting template
        greeting_text = GREETING_TEMPLATES[language]
        
        # Add some metadata about available languages
        available_langs = ", ".join(GREETING_TEMPLATES.keys())
        footer = f"\n\n(Available languages: {available_langs})"
        
        return types.GetPromptResult(
            description=f"Friendly greeting in {language}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=greeting_text + footer
                    )
                )
            ]
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")


# =============================================================================
# 5. SERVER LIFECYCLE MANAGEMENT
# =============================================================================

async def handle_initialization(options: InitializationOptions) -> None:
    """
    Handle server initialization.
    
    This function is called when the MCP client connects to the server.
    It can be used to set up any necessary resources or validate the
    connection.
    
    Args:
        options: Initialization options from the client
    """
    print(f"Hello World MCP Server initialized at {datetime.now()}", file=sys.stderr)
    print(f"Server capabilities: {SERVER_INFO['features']}", file=sys.stderr)


async def cleanup() -> None:
    """
    Cleanup function called when the server is shutting down.
    
    Use this to clean up any resources, close connections, etc.
    """
    print("Hello World MCP Server shutting down...", file=sys.stderr)


# =============================================================================
# 6. MAIN SERVER LOOP
# =============================================================================

async def main():
    """
    Main entry point for the MCP server.
    
    Sets up the server with stdio transport and runs the main loop.
    This function handles the connection lifecycle and error management.
    """
    try:
        # Set up stdio transport options
        options = mcp.server.stdio.StdioServerParameters(
            command="python",
            args=[__file__],
            env=None
        )
        
        print("Starting Hello World MCP Server...", file=sys.stderr)
        print(f"Server version: {SERVER_INFO['version']}", file=sys.stderr)
        
        # Run the server with stdio transport
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="hello-world-mcp",
                    server_version=SERVER_INFO["version"],
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
            
    except KeyboardInterrupt:
        print("Server interrupted by user", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        raise
    finally:
        await cleanup()


if __name__ == "__main__":
    """
    Entry point when running the server directly.
    
    This allows the server to be run with: python main.py
    """
    print("Hello World MCP Server starting up...", file=sys.stderr)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"Fatal server error: {e}", file=sys.stderr)
        sys.exit(1)
