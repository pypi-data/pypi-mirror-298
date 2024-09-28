import os
def init():
    import jnius_config
    jarpaths = [os.path.join("app_data", "jar"), "dd"]
    result = []
    for jarpath in jarpaths:
        if not os.path.exists(jarpath): return
        jars = os.listdir(jarpath)
        jars = [os.path.join(jarpath, item) for item in jars if item.endswith(".jar")]
        result = result + jars
    jnius_config.add_classpath(*result)
init()
def autoclass(cls):
    import jnius
    return jnius.autoclass(cls)
def invoke(cls, cls_params=None, func=None, func_params=[]):
    clazz = autoclass(cls)
    if cls_params is not None:
        clazz = clazz(*cls_params) if cls_params else clazz()
    if func is None: return clazz
    return getattr(clazz,func)(*func_params)