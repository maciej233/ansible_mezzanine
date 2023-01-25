try:
    from local_settings import *
except ImportError as e:
    if "local_settings" not in str(e):
        raise e