from mpmath import mp  # type: ignore

from .. import VERSION  # noqa: TID252

__version__ = VERSION

type MPFloat = mp.mpf  # pyright: ignore
type MPMatrix = mp.matrix  # pyright: ignore
