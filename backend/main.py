from flask import Flask

from flask_cors import CORS

from backend.routes.awakened_leveling_routes import awakened_leveling_bp
from backend.routes.chaos_res_crafting_routes import chaos_res_crafting_bp
from backend.routes.harvest_rolling_routes import harvest_rolling_bp
from backend.routes.reforge_influence_routes import reforge_influence_bp
from backend.routes.sanctum_rewards_routes import sanctum_rewards_bp
from backend.routes.six_linking_routes import six_linking_bp
from backend.routes.t17_maps_routes import t17_maps_bp

app = Flask(__name__)
cors = CORS(app, origins="http://127.0.0.1:3000")

app.register_blueprint(awakened_leveling_bp)
app.register_blueprint(chaos_res_crafting_bp)
app.register_blueprint(harvest_rolling_bp)
app.register_blueprint(reforge_influence_bp)
app.register_blueprint(sanctum_rewards_bp)
app.register_blueprint(six_linking_bp)
app.register_blueprint(t17_maps_bp)


# NEED TO MAKE CHANGES TO API_DATA to have them inherited to all data classes


# modify the price values of certain objects in api data

# is that all i need?

# changing amount per div can be converted
# all comes down to price

# percent outcomes should be constant and changed in the files

# only want to sometimes change to update prices
# store updated prices somewhere, database?


# one api endpoint per page to edit the variables used in those algorithms
# get retrieves both the variables and results

# post will update the variables and rerun the functions for each class

################################################################


if __name__ == "__main__":
    app.run(debug=True)
