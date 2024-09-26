"""Main entry point for the server"""

from .server import create_app

app = create_app()

if __name__ == "__main__":
    app = create_app()
