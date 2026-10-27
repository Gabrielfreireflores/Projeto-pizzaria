from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Roda o servidor local de desenvolvimento na porta 5000
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))