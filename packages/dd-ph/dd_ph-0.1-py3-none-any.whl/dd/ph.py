import json, os, re, datetime, hashlib, threading, io

class dynamic(object):
    def __init__(self, *args, **kwargs):
        dict.__init__(self.__dict__, *args, **kwargs)
    def __setattr__(self, key, value):
        self.__dict__[key] = value
    def __getattr__(self, key):
        return self.__dict__[key] if key in self.__dict__ else None
    def __getitem__(self, item):
        return self.__dict__[item] if item in self.__dict__ else None
    def __setitem__(self, item, value):
        self.__dict__[item] = value
    def __iter__(self):
        return self.__dict__.__iter__()
    def __repr__(self):
        return jh.Encode(self)

class JsonDateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, dynamic):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)
JsonDateEncoderDefault = JsonDateEncoder().default

class JsonHelper():
    def Encode(self, model):
        return json.dumps(model, default=JsonDateEncoderDefault, indent=2)
    def Unbox(self, pyobj):
        if isinstance(pyobj, list):
            return [self.Unbox(i) for i in pyobj]
        elif isinstance(pyobj, dict):
            newobj = dynamic(pyobj)
            for k in pyobj:
                newobj[k] = self.Unbox(pyobj[k])
            return newobj
        return pyobj
    def Decode(self, string):
        return self.Unbox(json.loads(string))
    def Msg(self, error, message, data):
        msg = dynamic()
        msg.error, msg.message, msg.data, msg.reload = error, message, data, 0 if error else 1
        return msg
    def Data(self, data):
        msg = self.Msg(0, None, data)
        msg.reload = 0
        return msg
    def Error(self, message, data=None):
        return self.Msg(1, message, data)
    def Success(self, message, data=None):
        return self.Msg(0, message, data)
    def Href(self, url, target="_blank"):
        msg = dynamic()
        msg.href, msg.target = url, target
        return msg
jh = JsonHelper()

class DDHelper():
    def __init__(self):
        self.dynamic = dynamic
    def stamp(self):
        import time
        return int(time.time()/1000)
    def re_findall(self, pattern, content, flags=0):
        if not content: return None
        return re.findall(pattern, content, flags)
    def re_find(self, pattern, content, idx=0):        
        findall = self.re_findall(pattern, content)
        return findall[0] if findall else None
    def matchobjs(self, pattern, content, flags=0):
        iters = re.finditer(pattern, content, flags) if isinstance(pattern, str) else pattern.finditer(content)
        matches, model = [m for m in iters], []
        for match in matches: model.append(dynamic(match.groupdict()))
        return model
    def post(self, url, **kvargs):
        from urllib import request, parse
        data = parse.urlencode(kvargs).encode()
        req =  request.Request(url, data=data)
        res = request.urlopen(req)
        return res.read().decode('utf-8')
    def get(self, url, **kvargs):
        from urllib import request, parse
        data = parse.urlencode(kvargs)
        if data:
            url = url + '?' + data if '?' not in url else url + '&' + data            
        req =  request.Request(url)
        res = request.urlopen(req)
        return res.read().decode('utf-8')
    def getmsg(self, url, **kvargs):
        from urllib.error import HTTPError, URLError
        msg = self.dynamic()
        try:
            msg.error = 0
            msg.data = self.get(url, **kvargs)
            msg.code = 200
            return msg
        except HTTPError as err:
            msg.error = 1
            msg.code = err.code
            msg.message = err.msg
            msg.data = err.fp.read().decode('utf-8')
            return msg
        except URLError as err:
            msg["error"] = 1
            msg["code"] = None
            msg["message"] = err.reason
            msg["data"] = None
            return msg
    def bytes2base64(self, bytes):
        import base64
        return str(base64.b64encode(bytes), 'utf-8')
    def base642bytes(self, b64):
        import base64
        return base64.b64decode(b64)
    def extend(self, dobj, *objs):
        for obj in objs:
            if isinstance(obj, dynamic):
                dobj.__dict__.update(obj.__dict__)
            else:
                dobj.__dict__.update(obj)
        return dobj
    def file2str(self, path, encoding='utf-8'):
        if not os.path.exists(path): return None
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    def str2file(self, content, path): 
        with open(path, 'w') as f:
            return f.write(content)
    def file2bytes(self, path):
        if not os.path.exists(path): return None
        with open(path, 'rb') as f:
            return f.read()
    def bytes2file(self, content, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            return f.write(content)
    def popen(self, argv, encoding='utf-8'):
        import subprocess
        child = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = child.stdout.read().decode(encoding)
        err = child.stderr.read().decode(encoding)
        return out, err
    def md5(self, str):
        m = hashlib.md5()
        b = str.encode(encoding='utf-8')
        m.update(b)
        return m.hexdigest()
    def md5file(self, filepath):
        m = hashlib.md5()
        b = self.file2bytes(filepath)
        m.update(b)
        return m.hexdigest()
    def omit(self, obj, atts):
        if isinstance(atts, str):
            atts = atts.split(",")
        result = dynamic()
        for key in obj:
            if key not in atts:
                result[key] = obj[key]
        return result
    def param(self, obj, urlencode=True, conn1="=", conn2="&"):
        kvs = [(key, obj[key]) for key in obj]
        kvs = sorted(kvs, key=lambda x:x[0])
        return conn2.join(["{0}{1}{2}".format(kv[0], conn1, kv[1]) for kv in kvs])
    def run(self, func, cin):
        if isinstance(cin, list) or isinstance(cin, tuple): return func(*cin)
        dct = {}
        co, dft = func.__code__, func.__defaults__
        for varname in co.co_varnames[:co.co_argcount]:
            dct[varname] = cin[varname]
        if dft:
            for item in zip(co.co_varnames[co.co_argcount-len(dft):co.co_argcount], dft):
                if dct[item[0]] is None: dct[item[0]] = item[1]
                elif isinstance(dct[item[0]], str):
                    typeName = type(item[1]).__name__
                    if typeName == "int":  dct[item[0]] = int(dct[item[0]])
                    if typeName == "float": dct[item[0]] = float(dct[item[0]])
                    if typeName == "bool": dct[item[0]] = self.str2bool(dct[item[0]])
        return func(**dct)
    def hmac_sha2(self, text, key):
        import hashlib, hmac
        appsecret = key.encode('utf-8')
        data = text.encode('utf-8')
        signature = hmac.new(appsecret, data, digestmod=hashlib.sha256).hexdigest()
        return signature
    def java(self, class_name):
        from dd.dd_java import autoclass
        return autoclass(class_name)
dd = DDHelper()

class DataHelper:
    def __init__(self, conn_fn, conn_params):
        self.conn_fn, self.conn_params = conn_fn, conn_params
    def CreateConnection(self):
        return self.conn_fn(**self.conn_params)
    def _execute(self, sql, args=[]):
        with self.CreateConnection() as conn:
            with conn.cursor() as curs:
                curs.execute(sql, args) if args else curs.execute(sql)
                result = ( [d[0] for d in curs.description ], curs.fetchall())
                conn.commit()
        return result
    def Objs(self, sql, args=[]):
        result = self._execute(sql, args)
        return [ dict(zip(result[0],row)) for row in result[1]]
    def Obj(self, sql, args=[]):
        entities = self.Objs(sql,args)
        return entities[0] if entities else None
    def Matrix(self, sql, args=[]):
        result = self._execute(sql, args)
        return [result[0]] + result[1]
    def List(self, sql, args=[]):
        result = self._execute(sql, args)
        return [ row[0] for row in result[1]]
    def Dict(self, sql, args=[]):
        result = self._execute(sql, args)
        return dict([ (row[0],row[1]) for row in result[1]])
    def Exec(self, sql, args=[]):
        conn = self.CreateConnection()
        curs = conn.cursor()
        curs.executemany(sql,args) if args and isinstance(args,list) and (isinstance(args[0],list) or isinstance(args[0],dict)) else curs.execute(sql,args)
        conn.commit(), curs.close(), conn.close()

setting = jh.Decode(dd.file2str("app.json") or "{}")

class MemoryCache():
    def __init__(self):
        self.Cache = {}
        self.lock = threading.Lock()
    def find(self, keyData, keySelector, dataSelector):
        key = keySelector(keyData)
        if key in self.Cache: return self.Cache[key]
        with self.lock:
            if key in self.Cache: return self.Cache[key]
            self.Cache[key] = data = dataSelector(keyData)
            return data
    def clear(self):
        self.Cache.clear()

class Job():
    def __init__(self):
        from concurrent.futures import ThreadPoolExecutor
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.jobs = {}
    def job(self, name, func, argv):
        func(*argv)
        if name in self.jobs:
            del self.jobs[name]
    def run(self, name, func, argv):
        self.clear()
        self.jobs[name] = self.executor.submit(self.job, name, func, argv)
        return self.jobs[name]
    def clear(self):
        for key in list(self.jobs.keys()):
            if self.jobs[key].done():
                del self.jobs[key]
job = Job()

appdata = dynamic()
appcache = MemoryCache()

class Engine():
    def __init__(self):
        self.store = dd.dynamic()
        self.cache = MemoryCache()
    def Keys(self):
        return tuple(self.store.__dict__.keys())
    def Source(self, name):
        return self.store[name].code
    def Set(self, name, code):
        model = dd.dynamic()
        model.name = name
        model.code = code
        model.md5 = dd.md5(code)
        self.store[name] = model
    def Sets(self, json):
        models = jh.Decode(json)
        for model in models:
            model.md5 = dd.md5(model.code)
            self.store[model.name] = model
    def Get(self, name):
        def fnKey(item):
            return item.md5
        def fnData(item):
            return self.Execute(item.code, { "ph": dynamic(globals()) })
        if not self.store[name]: return None
        return self.cache.find(self.store[name], fnKey, fnData)
    def Invoke(self, name, method, args):
        module = self.Get(name)
        func = module[method]
        return func(*args)
    def Compile(self, source, filename):
        code = compile(source, filename, "exec")
        return code
    def Execute(self, code, args={}):
        gl = dict()
        gl.update(args if isinstance(args,dict) else args.__dict__)
        exec(code, gl)
        return dynamic(gl)
eh = Engine()

requireCache = MemoryCache()
def require(filename, name='export'):
    def keyFn(keyData):
        filename = keyData
        filename = filename if filename.endswith(".py") else filename+'.py'
        return dd.md5(dd.file2str(filename))
    def dataFn(keyData):
        filename = keyData
        filename = filename if filename.endswith(".py") else filename+'.py'
        if not os.path.exists(filename): return None
        source = dd.file2str(filename)
        code = eh.Compile(source, filename)
        result = eh.Execute(code)
        return result
    result = requireCache.find(filename, keyFn, dataFn)
    return result[name] if result and result[name] else result

def fig2bytes(fig, fmt='svg'):
    with io.BytesIO() as buf:
        fig.savefig(buf, format=fmt)
        buf.seek(0)
        return buf.read()