connectionString = "mysql+pymysql://root:cong@localhost:3306/demo2"
def setup(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = connectionString
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'