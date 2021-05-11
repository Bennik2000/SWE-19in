import vereinswebseite

if __name__ == '__main__':
    app = vereinswebseite.create_app()

    with app.app_context():
        vereinswebseite.init_db()

    app.run(debug=True)
