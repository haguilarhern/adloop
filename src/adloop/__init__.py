"""AdLoop — MCP server connecting Google Ads + GA4 + codebase."""

import os
import sys

__version__ = "0.1.0"


def main() -> None:
    """Entry point for `adloop` console script.

    Routes to the setup wizard when called as ``adloop init``,
    otherwise starts the MCP server.

    Supports ``--transport`` flag for remote deployment:
      adloop --transport streamable-http
      adloop --transport sse
    Defaults to stdio if not specified.

    The HTTP host/port can be set via ADLOOP_HOST / ADLOOP_PORT env vars.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        from adloop.cli import run_init_wizard

        run_init_wizard()
    else:
        from adloop.server import mcp

        transport = "stdio"
        if "--transport" in sys.argv:
            idx = sys.argv.index("--transport")
            if idx + 1 < len(sys.argv):
                transport = sys.argv[idx + 1]

        if transport in ("streamable-http", "sse"):
            host = os.environ.get("ADLOOP_HOST", "0.0.0.0")
            port = int(os.environ.get("ADLOOP_PORT", "3000"))
            mcp.run(transport=transport, host=host, port=port)
        else:
            mcp.run()
