from api import app

import users
import slots
import patines

app.register_blueprint(users.users_api)
app.register_blueprint(slots.slots_api)
app.register_blueprint(patines.patines_api)


@app.route("/api/index")
def hello():
    return "GoPatines!"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)