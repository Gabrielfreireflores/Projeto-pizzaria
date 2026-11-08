from main import app
import os

if __name__ == '__main__':
    # Roda o servidor local de desenvolvimento na porta 5000
    app.run(debug=not app.config['PRODUCTION'], port=int(os.getenv("PORT", 5000)))
