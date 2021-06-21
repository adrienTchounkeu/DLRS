from Technipedia.App.Routes.AdminRoutes.LoadServices import loadApp as adminLoad
from Technipedia.App.Routes.UserWebRoutes.LoadServices import loadApp as userWebLoad
from Technipedia.App.Routes.UserMobileRoutes.LoadServices import loadApp as userMobileLoad


def loadApp(app):
    adminLoad(app)
    userWebLoad(app)
    userMobileLoad(app)