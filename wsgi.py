from pkg import create_app

application = create_app()
application.config["APPLICATION_ROOT"] = "/talentbridge"