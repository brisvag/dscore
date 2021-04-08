import pandas as pd

from . import get_all


results = {}
for server, function in get_all:
    data = function()
    results[server] = data

