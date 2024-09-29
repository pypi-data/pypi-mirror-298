import importlib


def class_loader(class_path: str):
    pkg, clazz_name = ".".join(class_path.split(".")[0:-1]), class_path.split(".")[-1]
    module = importlib.import_module(pkg)
    entry_clazz = getattr(module, clazz_name)
    return entry_clazz


def new_class(clazz, *args, **kwargs):
    if type(clazz) == str:
        return class_loader(class_path=clazz)(*args, **kwargs)
    else:
        return clazz(*args, **kwargs)
