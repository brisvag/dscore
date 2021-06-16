from .cspritz import get_cspritz_long, get_cspritz_short
from .disembl import get_disembl
from .disopred import get_disopred
from .disprot import get_disprot
from .globplot import get_globplot
from .iupred import get_iupred_long, get_iupred_short
from .pondr import get_pondr
from .prdos import get_prdos
from .seg import get_seg

from .foldindex import get_foldindex

from .jpred import get_jpred

sequence_disorder = {
    'cspritz_L': get_cspritz_long,
    'cspritz_S': get_cspritz_short,
    'disembl': get_disembl,
    'disopred': get_disopred,
    'disprot': get_disprot,
    'globplot': get_globplot,
    'iupred_L': get_iupred_long,
    'iupred_S': get_iupred_short,
    'pondr': get_pondr,
    'prdos': get_prdos,
    'seg': get_seg,
}

general_disorder = {
    'foldindex': get_foldindex,
}

# to finish
todo = (
    get_jpred,
)


by_speed = {'fast': ['disembl', 'disprot', 'globplot', 'iupred_S', 'iupred_L', 'pondr', 'seg']}
by_speed['normal'] = by_speed['fast'] + ['prdos', 'disopred']
by_speed['slow'] = by_speed['normal'] + ['cspritz_S', 'cspritz_L']
