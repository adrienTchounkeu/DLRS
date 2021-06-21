from Technipedia.App.Routes.UserMobileRoutes.CatServices import addCatServices
from Technipedia.App.Routes.UserMobileRoutes.LocServices import addLocServices
from Technipedia.App.Routes.UserMobileRoutes.OldPassServices import addOldPassServices
from Technipedia.App.Routes.UserMobileRoutes.OppServices import addOppServices
from Technipedia.App.Routes.UserMobileRoutes.PrefServices import addPrefServices
from Technipedia.App.Routes.UserMobileRoutes.UserServices import addUserServices


def loadApp(app):
    addCatServices(app)
    addLocServices(app)
    addOldPassServices(app)
    addOppServices(app)
    addPrefServices(app)
    addUserServices(app)