# Cache Return

This library provide a simple wrapper for custom functions to get the caching mechanism.

## Use cases and benefits

With the caching mechanism activated, the result of a sub-function will be cached in the dedicated folder in the initial run. And the in the following runs, the cached result will loaded to bypass the actual internal process of a function. 

This will be mainly useful for testing or debug tasks of larger projects with sophisticated sub-functions. As it will

1. Avoid the actual interanl function run, thus save resources (e.g. queries/calls to APIs or databases) and improve efficiency.
2. Achieve quicker testing processes and circles, as the reloading process is generally much faster than the function run.
3. Provide the possibility for "offline" debugging and investigation for the real cases, as the cached return result can be manually accessed for investigation.

## Examples

To add caching mechanism to a custom function, simply add the decorator wrapper to the function definition as below.

```
from cache_return import cache_return

@cache_return
def custom_function(arg_a, arg_b='default_value'):
    ... internal processes ...
    return results
```

Then custom function can be usage the same way as before. To activate its caching mechanism, simply provide an additional keyword argument `caching=True`.

```
# Before

return_result = custom_function(arg_a, arg_b='actual_value')

# After

return_result = custom_function(arg_a, arg_b='actual_value', caching=True)
```

To turn the caching mechanism off in the production code, you can either set the keyword argument as `caching=False`, or simple remove the `caching=True` keyword argument, as the default value `caching=False` will be used in this case.

The actual cached result will be saved in the auto-created folder `./_cache_` (sitting at the same directory as the top-level running script, not the script containing the custom function.), with the same name of the custom function as a pickle file

Then the cached result can be manully accessed in other places by the code below

```
import pickle

with open('./_cache_/custom_function.pkl', 'rb') as f:
    return_result = pickle.load(f)
```

#### Special note for environment with pandas version >= 2.0.0

The above custom investigation code has to be adjusted to the below code as 

```
import pandas as pd

with open('./_cache_/custom_function.pkl', 'rb') as f:
    return_result = pd.compat.pickle_compat.load('./_cache_/custom_function.pkl') 
```
Or, you can downgrade pandas to the 1.x series by `pip install pandas<2.0.0`, see the [stackoverflow topic here](https://stackoverflow.com/questions/75953279/modulenotfounderror-no-module-named-pandas-core-indexes-numeric-using-metaflo).

## Additional arguments

In some cases, if you only want to overwrite/update the cached result in the new function run, you can achieve this by set the `flushing` keyword argument as `flushing=True`.

By default the cached result will be save under directory `./_cache_`. An alternative directory `custom_dir` can be set by the argument `cache_path` as `cache_path=custom_dir`. Such a directory will be automatically created if it does not exist.