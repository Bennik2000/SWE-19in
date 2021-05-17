import vereinswebseite

if __name__ == '__main__':
    app = vereinswebseite.create_app()

    with app.app_context():
        vereinswebseite.create_and_fill_db()

    app.run(debug=True)
