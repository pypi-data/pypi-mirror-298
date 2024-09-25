
import functools
import pandas as pd
import os
import pickle

# note: this function require the cached module function names to be unique
# note: this function can be only applied to functions returning dataframe now 

def cache_return(_func=None):
    def decorator(func):
        func_name = func.__name__
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            caching = kwargs.pop('caching', False)
            flushing = kwargs.pop('flushing', False)
            cache_path = kwargs.pop('cache_path', './_cache_')

            if caching:
                if not os.path.exists(cache_path):
                    os.makedirs(cache_path)

                # dir_path = os.path.dirname(os.path.realpath(__file__))
                pkl_path = f'{cache_path}/{func_name}.pkl'
                if os.path.exists(pkl_path) and not flushing:
                    with open(pkl_path, 'rb') as file:
                        df_value = pd.compat.pickle_compat.load(file)
                        # df_value = pickle.load(file)

                    print(f'[INFO]: the value of function [{func_name}] has been obtained from {cache_path}!')
                    return df_value
            
            df_value = func(*args, **kwargs)
            
            if caching:
                with open(pkl_path, 'wb') as file:
                    pickle.dump(df_value, file)
                print(f'[INFO]: the value of function [{func_name}] has been cached under {cache_path}!')
            
            return df_value
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)