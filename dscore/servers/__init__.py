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

sequence_disorder = (
    get_cspritz_long, get_cspritz_short,
    get_disembl,
    get_disopred,
    get_disprot,
    get_globplot,
    get_iupred_long, get_iupred_short,
    get_pondr,
    get_prdos,
    get_seg,
)

general_disorder = (
    get_foldindex,
)

# to finish
todo = (
    get_jpred,
)
