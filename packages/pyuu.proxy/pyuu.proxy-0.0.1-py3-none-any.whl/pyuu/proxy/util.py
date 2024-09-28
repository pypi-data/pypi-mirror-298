

def recursive_update(a, b, method_name='update'):
    for key, value in b.items():
        if isinstance(value, dict) and key in a and isinstance(a[key], dict):
            recursive_update(a[key], value, method_name)
        else:
            if hasattr(a.get(key), method_name):
                getattr(a[key], method_name)(value)
            else:
                a[key] = value






