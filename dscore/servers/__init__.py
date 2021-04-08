from .cspritz import get_cspritz
from .disembl import get_disembl
from .disopred import get_disopred
from .disprot import get_disprot
from .foldindex import get_foldindex
from .globplot import get_globplot
from .iupred import get_iupred
from .jpred import get_jpred
from .pondr import get_pondr
from .prdos import get_prdos
from .seg import get_seg


get_functions = {
    'cspritz': get_cspritz,
    'disembl': get_disembl,
    'disopred': get_disopred,
    'disprot': get_disprot,
    'foldindex': get_foldindex,
    'globplot': get_globplot,
    'iupred': get_iupred,
    'jpred': get_jpred,
    'pondr': get_pondr,
    'prdos': get_prdos,
    'seg': get_seg,
}
