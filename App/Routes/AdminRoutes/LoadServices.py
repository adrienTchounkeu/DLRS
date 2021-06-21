from Technipedia.App.Routes.AdminRoutes.CatServices import addCatServices
from Technipedia.App.Routes.AdminRoutes.LocServices import addLocServices
from Technipedia.App.Routes.AdminRoutes.OldPassServices import addOldPassServices
from Technipedia.App.Routes.AdminRoutes.OppServices import addOppServices
from Technipedia.App.Routes.AdminRoutes.PrefServices import addPrefServices
from Technipedia.App.Routes.AdminRoutes.AdminServices import addUserServices


def loadApp(app):
    addCatServices(app)
    addLocServices(app)
    addOldPassServices(app)
    addOppServices(app)
    addPrefServices(app)
    addUserServices(app)