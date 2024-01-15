from __init__ import app
import os
from whitenoise import WhiteNoise

port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,debug=False)
    app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
    # register your blueprints
    # app.register_blueprint(frontend)

    # add whitenoise
    app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
            