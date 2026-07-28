import os

from app import create_app

my_app = create_app()

if __name__ == "__main__":
    my_app.run(
        port=os.getenv("PORT", 5200), debug=os.getenv("DEBUG", False), host=os.getenv("HOST", "0.0.0.0")
    )
