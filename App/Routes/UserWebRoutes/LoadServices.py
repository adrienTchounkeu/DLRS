from Technipedia.App.Routes.UserWebRoutes.CatServices import addCatServices
from Technipedia.App.Routes.UserWebRoutes.LocServices import addLocServices
from Technipedia.App.Routes.UserWebRoutes.OldPassServices import addOldPassServices
from Technipedia.App.Routes.UserWebRoutes.OppServices import addOppServices
from Technipedia.App.Routes.UserWebRoutes.PrefServices import addPrefServices
from Technipedia.App.Routes.UserWebRoutes.UserServices import addUserServices


def loadApp(app):
    addCatServices(app)
    addLocServices(app)
    addOldPassServices(app)
    addOppServices(app)
    addPrefServices(app)
    addUserServices(app)
