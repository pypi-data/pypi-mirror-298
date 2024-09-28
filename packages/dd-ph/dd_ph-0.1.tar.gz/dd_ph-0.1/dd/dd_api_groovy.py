from dd.ph import *
import dd.dd_java as java
app = java.autoclass("dd.groovy.App")
def Set(name, code):
    app.set(name, code)
def Sets(json):
    models = jh.Decode(json)
    for model in models:
        Set(model.name, model.code)
def Invoke(name, method, argv):
    if not isinstance(argv, str): argv = jh.Encode(argv)
    return jh.Decode(app.invokeJson(name, method, argv))