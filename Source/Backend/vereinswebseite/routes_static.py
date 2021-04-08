from Source.Backend.vereinswebseite import app


@app.route('/static/main.css')
def style():
    return app.send_static_file('main.css')

