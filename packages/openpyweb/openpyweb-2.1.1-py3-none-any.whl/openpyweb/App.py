###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###


from openpyweb.Request import Request
from openpyweb.Session import Session
from openpyweb.Editor import Template
from openpyweb.Config import Config
from openpyweb.Log import Log
from openpyweb import Lang
from openpyweb.Version import *
from openpyweb.Core.env import env
from openpyweb.util.Variable import Variable
from openpyweb.Functions import url, iteration
from openpyweb.Controllers import Controllers
import os
import sys
import importlib
import glob
import  json
import inspect



global host

if os.path.isdir(os.path.join(os.getcwd(), 'public')):
    host = os.path.join(os.getcwd())  # os.path.dirname(os.getcwd())

else:
    host = os.path.join(os.path.dirname(os.getcwd()))

controllerpath = os.path.join(host, 'controller')
error_page_class = os.path.join(controllerpath,"ErrorController.py")

header_response_page = {
    '301': 'error/page301',  # Bad Request
    '302': 'error/page302',  # Bad Request
    '307': 'error/page307',  # Bad Request
    '400': 'error/page400',  # Bad Request
    '404': 'error/page404',  # Not Found
    '405': 'error/page405',  # Method Not Allowed
    '500': 'error/page500',  # Internal Server Error

}

data_c = {}

class App(env, Config, Variable):

    def __getattr__(self, item):
        return item

    def __init__(self, routers="", routes="", getpath="", getrouters=""):

        self.routers = routers
        self.routes = routes
        self.getpath = getpath
        self.codereponse = 200
        self.getrouters = getrouters
        self.getDB = ""
        self.Request = Request
        self.Session = Session
        self.methodprefix = ""
        self.actions = ""
        self.controllers = ""
        self.controller = ""
        self.dbDriver = None
        self.Config = None
        self.url = ""
        self.params = ""
        self.key = ""
        self.vpathf = ""
        self.languages = ""
        self.Driver = ""
        self.formData = None
        self.server_obj = None
        self.datag = {}

    def getRouters(self):

        return self.routers

    def getPath(self):
        return self.getpath

    def runs(self, formData=None, serverobj=None):
        self.formData = formData
        self.server_obj = serverobj
        return self.initial()

    def initial(self):
        if self.out("SERVER_SOFTWARE") != AUTHOR:
            import cgitb
            cgitb.enable()

        self.default("Framework", AUTHOR)
        self.default("X-Version", VERSION_TEXT)
        self.getrouters = self.envrin('route')
        self.controllers = Controllers()
        self.methodprefix = self.controllers._getMethodPrefix()
        self.actions = self.controllers._getActions()
        self.uri = self.controllers._getUri()
        self.controller = self.controllers._getControllers()
        self.routers = self.controllers._getRoutes()
        self.languages = self.controllers._getLanguages()
        self.params = self.controllers._getParams()
        langs = Lang.Lang(self.languages)
        langs.loadLang()

        controlUri = []


        if PYVERSION_MA >= 3:
            lrounters = self.getrouters.items()
        else:
            lrounters = self.getrouters.iteritems()

        for k, getRouter in lrounters:

            if self.controller == k:
                controlUri = getRouter.split('@')

        self.routerend()

        if len(controlUri) != 0:

            if 'controller' in controlUri[0].lower():

                controllersClass = str(controlUri[0].lower()).replace('controller', '').capitalize() + 'Controller'
            else:
                controllersClass = str(controlUri[0]).capitalize() + 'Controller'

            if ':' not in controlUri[1]:
                controllersMethods = str(controlUri[1])

            else:
                getMapPara = controlUri[1].split(':')

                controllersMethods = str(getMapPara[0])

        else:

            if str(self.controller[0]) == '?':
                if self.controllers.default_controllers != "":
                    controllersClass = str(self.controllers.default_controllers).capitalize() + 'Controller'

                else:
                    controllersClass = "IndexController"
            else:

                controllersClass = str(self.controller[0]).capitalize(
                ) + str(self.controller[1:]) + 'Controller'

            controllersMethods = str(self.actions)

        if controllersMethods != "":
            self.actions = controllersMethods

        controllers = os.path.join(controllerpath, "%s.py" % controllersClass)

        if os.path.isfile(controllers) == True:

            if __name__ == '__main__':
                spac = ""
            if os.path.isfile(controllers) == True:

                if sys.version_info.major <= 2:

                    return self.strClass(controllerpath, controllersClass)
                else:

                    return self.strClass3(controllerpath, controllersClass)

        else:
            if controllersClass !="Favicon.icoController" and controllersClass != "PublicController":
                Log(controllerpath).error('Controller does not exist ' + str(controllersClass))
                return self.errorP('405')

    def iterate(self, value=[], name='pid'):
        return iteration.iteration().iteri(value, itr=name)


    def URL(self, path='', lang=False):
        return url.url().url(path=path, lang=lang)

    def errorP(self, code, replace=""):
        getErrorP = self.envrin('error')

        if os.path.isfile(os.path.join(host,"routes.py")) == True:
            sys.path.append(host)
            import routes as route
            if len(route.route.getError()) > 0:

                for i, redirect in enumerate(route.route.getError()):

                    if len(route.route.getError()) > 0:
                        toeroor = route.route.getError()[i]
                    if len(route.route.getErrorControl()) > 0:
                        fromroute = route.route.getErrorControl()[i]

                    if len(route.route.getCode()) > 0:
                        code = route.route.getCode()[i]

                    if len(route.route.getLink()) > 0:
                        link = route.route.getLink()[i]

                    if fromroute == self.controller:
                        return self.redirect(location=toeroor, link=bool(link), code=code)

        pageCode = "page{code}".format(code=code)
        if os.path.isdir(os.path.join(os.getcwd(), 'public')):
            if self.out("SERVER_SOFTWARE") == AUTHOR:
                    if getErrorP != '':
                        errorP = getErrorP

                        if errorP.get(code, '') != '':
                            self.put(status=code)
                            _error_l = errorP.get(code, '')
                            if _error_l != '':
                                re_url = self.URL(_error_l, lang=True)
                        else:
                            if os.path.isfile(self.error_page_html(code)) == True:
                                re_url = self.URL("/error/{code}".format(code=pageCode), lang=True)
                        return code, re_url

        if getErrorP != '':

            errorP = getErrorP
            if errorP.get(code, '') != '':
                self.put(status=code)
                _error_l = errorP.get(code, '')
                if _error_l != '':
                    self.default("SERVER_SOFTWARE", "")
                    return self.redirect(_error_l, link=True, code=code, lang=True)
            else:
                self.default("SERVER_SOFTWARE", "")
                if os.path.isfile(self.error_page_html(code)) == True:
                    return self.redirect("/error/{code}".format(code=pageCode), code=code, lang=True)

        else:
            self.default("SERVER_SOFTWARE", "")
            if os.path.isfile(error_page_class) == True:
                return self.redirect(self.URL("/error/{code}".format(code=pageCode)))

    def envrin(self, key):
        env = self._e()
        self.add(env)
        return self.get(key, '')

    def DB(self):

        self.dbDriver = self.envrin('dbConnect')
        if self.dbDriver.get("driver", '') == "MYSQL":
            from openpyweb.Driver.DB.MYSQL.MYSQL import MYSQL
            self.getDB = MYSQL(self.dbDriver)
            self.Driver = "MYSQL"
            return self.getDB

        if self.dbDriver.get("driver", '') == "SQLite":
            from openpyweb.Driver.DB.SQLite.SQLite import SQLite
            self.getDB = SQLite(self.dbDriver)
            self.Driver = "SQLite"
            return self.getDB

        if self.dbDriver.get("driver", '') == "Oracle":
            from openpyweb.Driver.DB.Oracle.Oracle import Oracle
            self.getDB = Oracle(self.dbDriver)
            self.Driver = "Oracle"
            return self.getDB

        if self.dbDriver.get("driver", '') == "pyPgSQL":
            from openpyweb.Driver.DB.pyPgSQL.pyPgSQL import pyPgSQL
            self.getDB = pyPgSQL(self.dbDriver)
            self.Driver = "pyPgSQL"
            return self.getDB

    def strClass(self, p=None, c=None):

        try:
            sys.path.append(p)
            ms = str(self.actions)
            md = importlib.import_module(c)
            self.default("REDIRECT_REDIRECT_STATUS", 200)
            self.default("REDIRECT_STATUS", 200)
            return self.strMethod(p, md, ms)

        except Exception as err:
            Log(os.path.join(p,'%s.py'%c)).critical(err)

            return self.errorP('404')

    def strMethod(self, p, c=None, mv=None):
        gmodule = []
        Request = self.Request(prform=self.formData)
        Session = self.Session(prsee=self.server_obj)

        try:
            m = mv.split("?")[0]
        except Exception as err:
            m = mv
        try:
            return getattr(c, m)(Request, Session)
        except Exception as err:
            try:
                return getattr(c, m)(Session, Request)
            except Exception as err:
                try:
                    return getattr(c, m)(Request)
                except Exception as err:
                    try:
                        return getattr(c, m)(Session)
                    except Exception as err:
                        try:
                            return getattr(c, m)()
                        except Exception as err:
                            Log(os.path.join(p,'%s.py'%c)).critical(err)
                            return self.errorP('404')

    def strClass3(self, p=None, c=None):

        try:
            sys.path.append(p)
            ms = str(self.actions)
            importlib._RELOADING
            md = importlib.import_module(c, ms)
            self.default("REDIRECT_REDIRECT_STATUS", 200)
            self.default("REDIRECT_STATUS", 200)
            return self.strMethod(p, md, ms)

        except Exception as err:
            Log(os.path.join(p,'%s.py'%c)).critical(err)
            return self.errorP('404')

    def redirect(self, location='/', link=False, code="307", lang=False, method="GET"):

        if self.out("SERVER_SOFTWARE") == AUTHOR:

            if link == True:
                location_d = self.URL(location, lang)
            else:
                location_d = location
            self.put(redirect_url=location_d, status=code, method=method)
            return code, location_d
        else:

            if link == True:
                location_d = self.URL(location, lang)
            else:
                location_d = location

            self.default("REDIRECT_STATUS", code)
            self.default("REDIRECT_REDIRECT_STATUS", code)
            self.default("REQUEST_METHOD", method)
            print("Location: {location}".format(location=location_d))
            print()

    def referer(self, location='/', link=False, code="301", lang=False, method="GET"):
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            if link == True:
                location_d = self.URL(location, lang)
            else:
                location_d = location
            self.put(referral=self.out('HTTP_REFERER', location_d), redirect_url=location_d, status=code, method=method)
            return code, self.out('HTTP_REFERER', location_d) if self.out('HTTP_REFERER', location_d) != "" else location_d

        else:
            if link == True:
                location_d = self.URL(location, lang)
            else:
                location_d = location
            self.default("REDIRECT_STATUS", code)
            self.default("REDIRECT_REDIRECT_STATUS", code)
            self.default("REQUEST_METHOD", method)
            print("Location: {location}".format(location=self.out('HTTP_REFERER', location_d)))
            print()

    @staticmethod
    def header(p=0, type="text/html"):

        try:
            import imp
            imp.reload()
        except Exception:
            import importlib
            importlib.reload(sys)

        if os.path.isdir(os.path.join(os.getcwd(), 'public')) == False:
            if self.out("SERVER_SOFTWARE") != AUTHOR:
                print("Content-type: {type}\r\n".format(type=type))  # \r\n\r\n
                if p > 0:
                    for x in range(p):
                        print("")
        else:
            return

    def Jdumps(self, strings):

        try:
            return json.dumps(strings)
        except Exception as err:
            return strings

    def Jloads(self, strings):

        try:
            return json.loads(strings)
        except Exception as err:
            return strings


    def XHreponse(self, dataString, ctype=""):
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            self.header(type=ctype)
            return dataString
        else:

            for mime in MIME_TYPES:
                if str(mime["ext"]).replace(".", "") == ctype or str(mime["ext"]).replace(".", "") == ctype:
                    ctype = mime["type"]
            self.header(type=ctype)
            print(dataString)

    def views(self, pathf="", datag={}, datal={}):
        data_c.update(datag)

        if pathf == "":
            pathf = self.getDefaultViewPath()

        pathfhtml = os.path.join(host, 'views', "%s.html" % pathf)
        html = ""
        if os.path.isfile(pathfhtml) == False:
            Log(os.path.join(host, 'views')).critical('Cannot find file {}'.format(pathf + ".html"))

            return self.errorP('404')

        else:
            output = str('<!-- {} -->\n'.format(AUTHOR)) + self.read_html(os.path.join(host,'views'), pathf, data_c) + str('\n<!-- {} {} -->'.format(AUTHOR, VERSION_TEXT))
            if os.path.isdir(os.path.join(os.getcwd(),'public')):
                # print(os.environ)
                return output

            else:
                self.header()
                print(output)


    def jsonify(self, value='', error='', indent=4, code=200):
        try:
            _json = json.dumps(value)
            parsed =  json.loads(_json)
            self.default("REDIRECT_REDIRECT_STATUS", code)
            self.default("REDIRECT_STATUS", code)
            if error != '':
                parsed = {
                    'error': error,
                    'code': '403'
                }
        except Exception as e:
            parsed = {
                    'error': error,
                    'code': '403'
            }
            self.default("REDIRECT_REDIRECT_STATUS", 403)
            self.default("REDIRECT_STATUS", 403)

        if self.out("SERVER_SOFTWARE") == AUTHOR:
            return ('SetWriter', code, json.dumps(parsed, indent=indent), 'application/json')
        else:
            self.header(type="application/json")
            print(json.dumps(parsed, indent=indent))

    def read_html(self, template_dir, engine, context={}):
        data_c.update(context)
        html_file_path = os.path.join(template_dir, "%s.html" % engine)
        try:
            with open(html_file_path, encoding='utf-8') as html_file:
                html = html_file.read()

            return Template.Template(html).render(**data_c)

        except Exception as err:

            Log(str(os.path.join(template_dir, "%s.html" % engine))).error(err)
            return ""

    def getDefaultViewPath(self):

        router = self.Router.getRoutes()  # Routers.getRoutes()

        if router == "":
            rout = ""
        controllerDirectory = self.Router.getControllers()

        templateName = os.path.join(str(self.Router.getMethodPrefix()), 'views', "%s.html" % str(self.Router.getAction()))

        return templateName

    def error_page_html(self, code):
        return os.path.join(host, 'views', "%s.html" % code)

    def loadmodule(self):

        path = [os.path.join(str(os.path.dirname(__file__)), "Functions"), os.path.join(host, "model")]
        listpath = [path[0], path[1]]

        i = 0
        lclass = {}

        for pl in listpath:

            current_dir = os.path.join(pl)

            current_module_name = os.path.splitext(
                os.path.basename(current_dir))[0]

            for file in glob.glob(os.path.join(current_dir + "/*.py")):
                name = os.path.splitext(os.path.basename(file))[0]

                i = i + 1
                # Ignore __ files

                if name.startswith("__init__"):
                    continue
                if name != "__init__":
                    lclass0 = {name: name}
                    lclass.update(lclass0)

        if PYVERSION_MA <= 2:
            item = lclass.iteritems()
        else:
            item = lclass.items()
        result = {}
        for key, value in item:
            if value not in result.values():
                result[key] = value

        return result

    def routerend(self):
        if os.path.isfile(os.path.join(host,"routes.py")) == True:
            sys.path.append(host)
            import routes as route
            toroute, fromroute = "", ""

            if len(route.route.getRouter()) > 0:

                for i, redirect in enumerate(route.route.getCode()):
                    if len(route.route.getRediret()) > 0:
                        toroute = route.route.getRediret()[i]
                    if len(route.route.getDespatch()) > 0:
                        fromroute = route.route.getDespatch()[i]
                    if fromroute == self.controller:

                        self.redirect(location=toroute,
                                      link=True, code=redirect)

                for i, route_c in enumerate(route.route.getRouter()):

                    uri = self.uri
                    while("" in uri):
                        try:
                            uri.clear("")
                        except Exception as err:
                            uri.remove("")


                    if self.languages in uri:
                        uri.pop(0)

                    sltp  = str(route_c).split("/")
                    luri = ""
                    if len(uri) > 0:

                        luri = "/".join(uri[0:len(sltp)])

                    else:
                        luri = str(uri)

                    if luri == route_c:
                        routes_l = route_c


                        if len(route.route.getController()) > 0:
                            self.controller = route.route.getController()[i]

                        if len(route.route.getAction()) > 0:
                            self.actions = route.route.getAction()[i]

                        if len(route.route.getRouter()) > 0:
                            self.routers = route.route.getRouter()[i]
                        if len(route.route.getMethod()) > 0:
                            self.method = route.route.getMethod()[i]

                            if self.method != "":
                                if self.method != self.out("REQUEST_METHOD", ""):
                                    Log().error(str(str(self.controller).capitalize()) + "Controller/" + str(
                                        self.actions) + " Requires " + self.method)

                                    return self.errorP('400')
