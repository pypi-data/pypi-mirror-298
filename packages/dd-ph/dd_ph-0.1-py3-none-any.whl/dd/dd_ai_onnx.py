from dd.ph import *
import io, time
store = dd.dynamic()
prefix = "dd_ai_onnx."
def Sets(json):
    global store
    models = jh.Decode(json)
    codes = []
    for model in models:
        store[model.okey] = model
        codes.append({"name": prefix + model.okey, "code": model.opy})
    eh.Sets(jh.Encode(codes))

sessionCache = MemoryCache()
def InferenceSession(name):
    import onnxruntime
    def fnKey(key):
        return key.omodel_filepath
    def fnData(key):
        if key.oep == 1:
            providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
        else:
            providers=['CPUExecutionProvider']
        session = onnxruntime.InferenceSession(key.omodel_filepath, providers=providers)
        return session
    key = store[name]
    if not key.omodel_filepath: return None
    return sessionCache.find(key, fnKey, fnData)

def InferenceModule(name):
    return eh.Get(prefix+name)

def ElapsedInterval(elapsed):
    elapsed.Total = round(elapsed.Postprocess, 2)
    elapsed.Postprocess = round(elapsed.Postprocess - elapsed.Infer, 2)
    elapsed.Infer = round(elapsed.Infer - elapsed.Preprocess, 2)
    elapsed.Preprocess = round(elapsed.Preprocess - elapsed.LoadSource, 2)
    elapsed.LoadSource = round(elapsed.LoadSource, 2)
    return elapsed

def Run(name, source):
    meta = store[name]
    module, session = InferenceModule(name), InferenceSession(name)
    start = time.time()
    ctx, elapsed, result = dd.dynamic(), dd.dynamic(), dd.dynamic()
    ctx.elapsed, ctx.session = elapsed, session
    if meta.input_type == 'image':
        from PIL import Image
        bytes_stream = io.BytesIO(source)
        ctx.source = Image.open(bytes_stream)
    else:
        ctx.source = source
    elapsed.LoadSource = (time.time() - start) * 1000
    if module.preprocess:
        ctx.input = dd.run(module.preprocess, ctx)
    else:
        ctx.input = ctx.source
    elapsed.Preprocess = (time.time() - start) * 1000
    if module.process:
        ctx.output = dd.run(module.process, ctx)
    else:
        input_name = session.get_inputs()[0].name
        ctx.output = session.run([], {input_name: ctx.input })
    elapsed.Infer = (time.time() - start) * 1000
    if module.postprocess:
        ctx.result = dd.run(module.postprocess, ctx)
    else:
        ctx.result = ctx.output
    elapsed.Postprocess = (time.time() - start) * 1000
    result.result = ctx.result
    result.elapsed = ElapsedInterval(elapsed)
    return result