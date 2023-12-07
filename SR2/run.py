from app import create_app

a = create_app()

if __name__ == "__main__":
    a.run(debug=True)