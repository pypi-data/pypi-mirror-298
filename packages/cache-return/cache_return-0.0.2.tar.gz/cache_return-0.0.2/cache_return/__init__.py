
import functools
import pandas as pd
import os
import pickle

# note: this function require the cached module function names to be unique
# note: this function can be only applied to functions returning dataframe now 
# ref: jupyterhub/data-admin/projects/charter_house_hvac_investigation

def cache_return(_func=None):
    def decorator(func):
        func_name = func.__name__
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            caching = kwargs.pop('caching', False)

            if caching:
                if not os.path.exists('./_cache_'):
                    os.makedirs('./_cache_')

                # dir_path = os.path.dirname(os.path.realpath(__file__))
                pkl_path = f'./_cache_/{func_name}.pkl'
                if os.path.exists(pkl_path):
                    with open(pkl_path, 'rb') as file:
                        df_value = pd.compat.pickle_compat.load(file)
                        # print('_df_value: ', _df_value)
                        # df_value = pickle.load(file)

                    print(f'[INFO]: the value of function [{func_name}] has been obtained from ./_cache_!')
                    return df_value
            
            df_value = func(*args, **kwargs)
            
            if caching:
                with open(pkl_path, 'wb') as file:
                    pickle.dump(df_value, file)
                print(f'[INFO]: the value of function [{func_name}] has been cached under ./_cache_!')
            
            return df_value
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)