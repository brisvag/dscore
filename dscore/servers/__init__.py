# OBSOLETE:
# from .cspritz import get_cspritz_long, get_cspritz_short

from .disembl import get_disembl
from .disopred import get_disopred
from .disprot import get_disprot
from .globplot import get_globplot
from .iupred import get_iupred_long, get_iupred_short
from .pondr import get_pondr
from .prdos import get_prdos
from .espritz import get_espritz_xray, get_espritz_nmr, get_espritz_disprot
from .metapredict import get_metapredict
from .jpred import get_jpred

from .foldindex import get_foldindex

from .seg import get_seg

sequence_disorder = {
    'disembl': get_disembl,
    'disopred': get_disopred,
    'disprot': get_disprot,
    'espritz_disprot': get_espritz_disprot,
    'espritz_nmr': get_espritz_nmr,
    'espritz_xray': get_espritz_xray,
    'foldindex': get_foldindex,
    'globplot': get_globplot,
    'iupred_L': get_iupred_long,
    'iupred_S': get_iupred_short,
    'jpred': get_jpred,
    'metapredict': get_metapredict,
    'pondr': get_pondr,
    'prdos': get_prdos,
}

sequence_complexity = {
    'seg': get_seg,
}

by_speed = {'fast': ['disembl', 'disprot', 'globplot', 'iupred_S', 'iupred_L', 'pondr', 'espritz_xray', 'espritz_nmr', 'espritz_disprot', 'metapredict', 'foldindex']}
by_speed['normal'] = by_speed['fast'] + ['prdos', 'disopred']
by_speed['slow'] = by_speed['normal'] + ['jpred']

assert all(s in sequence_disorder for servers in by_speed.values() for s in servers)
