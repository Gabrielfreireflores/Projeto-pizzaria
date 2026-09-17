from app import create_app

app = create_app()

if __name__ == '__main__':
    # Roda o servidor local de desenvolvimento na porta 5000
    app.run(debug=True, port=5000)