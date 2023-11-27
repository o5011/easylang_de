from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class Genus(Enum):
    M = "m"
    F = "f"
    N = "n"


class Kasus(Enum):
    NOM = "nom"
    GEN = "gen"
    DAT = "dat"
    ACC = "acc"


class Numerus(Enum):
    SG = "sg"
    PL = "pl"


@dataclass
class AllowedMorph:
    genus: Genus
    kasus: Kasus
    numerus: Numerus


class GenusResolver:
    def __init__(self, *args):
        self.allowed_morphs: List[AllowedMorph] = args

    def get_possible_genera(self, kasus: Kasus, numerus: Numerus) -> List[Genus]:
        ret = []
        for morph in self.allowed_morphs:
            if (
                morph.kasus == kasus
                and morph.numerus == numerus
                and morph.genus is not None
            ):
                ret.append(morph.genus)
            elif morph.kasus == kasus and morph.genus is None:
                ret.append(Genus.M)
                ret.append(Genus.F)
                ret.append(Genus.N)

        ret = list(set(ret))
        return ret

    def _check_possible_genera(
        self, kasus: Kasus, numerus: Numerus, genus: Genus
    ) -> bool:
        genera = self.get_possible_genera(kasus, numerus)
        if genera == []:
            return True
        else:
            return genus in genera

    def check_possible_genera(
        self, kasus: Kasus, numerus: Numerus, genus: Union[Genus, List[Genus]]
    ) -> bool:
        if isinstance(genus, list):
            for g in genus:
                if self._check_possible_genera(kasus, numerus, g):
                    return True
            return False
        else:
            return self._check_possible_genera(kasus, numerus, genus)


RESOLVERS = {
    "der": GenusResolver(
        AllowedMorph(Genus.M, Kasus.NOM, Numerus.SG),
        AllowedMorph(Genus.F, Kasus.DAT, Numerus.SG),
        AllowedMorph(Genus.F, Kasus.GEN, Numerus.SG),
        AllowedMorph(None, Kasus.GEN, Numerus.PL),
    ),
    "derselben": GenusResolver(
        AllowedMorph(Genus.F, Kasus.DAT, Numerus.SG),
        AllowedMorph(Genus.F, Kasus.GEN, Numerus.SG),
        AllowedMorph(None, Kasus.GEN, Numerus.PL),
    ),
    "die": GenusResolver(
        AllowedMorph(Genus.F, Kasus.NOM, Numerus.SG),
        AllowedMorph(Genus.F, Kasus.ACC, Numerus.SG),
        AllowedMorph(None, Kasus.NOM, Numerus.PL),
        AllowedMorph(None, Kasus.ACC, Numerus.PL),
    ),
    "dieselbe": GenusResolver(
        AllowedMorph(Genus.F, Kasus.NOM, Numerus.SG),
        AllowedMorph(Genus.F, Kasus.ACC, Numerus.SG),
    ),
    "dieselben": GenusResolver(
        AllowedMorph(None, Kasus.NOM, Numerus.PL),
        AllowedMorph(None, Kasus.ACC, Numerus.PL),
    ),
    "diejenigen": GenusResolver(
        AllowedMorph(None, Kasus.NOM, Numerus.PL),
        AllowedMorph(None, Kasus.ACC, Numerus.PL),
    ),
    "das": GenusResolver(
        AllowedMorph(Genus.N, Kasus.NOM, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.ACC, Numerus.SG),
    ),
    "dasselbe": GenusResolver(
        AllowedMorph(Genus.N, Kasus.NOM, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.ACC, Numerus.SG),
    ),
    "den": GenusResolver(
        AllowedMorph(Genus.M, Kasus.ACC, Numerus.SG),
        AllowedMorph(None, Kasus.DAT, Numerus.PL),
    ),
    "denselben": GenusResolver(
        AllowedMorph(Genus.M, Kasus.ACC, Numerus.SG),
        AllowedMorph(None, Kasus.DAT, Numerus.PL),
    ),
    "dem": GenusResolver(
        AllowedMorph(Genus.M, Kasus.DAT, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.DAT, Numerus.SG),
    ),
    "demselben": GenusResolver(
        AllowedMorph(Genus.M, Kasus.DAT, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.DAT, Numerus.SG),
    ),
    "deren": GenusResolver(
        AllowedMorph(Genus.F, Kasus.GEN, Numerus.SG),
        AllowedMorph(None, Kasus.GEN, Numerus.PL),
    ),
    "dessen": GenusResolver(
        AllowedMorph(Genus.M, Kasus.GEN, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.GEN, Numerus.SG),
    ),
    "des": GenusResolver(
        AllowedMorph(Genus.M, Kasus.GEN, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.GEN, Numerus.SG),
    ),
    #
    "beide": GenusResolver(
        AllowedMorph(None, Kasus.NOM, Numerus.PL),
        AllowedMorph(None, Kasus.ACC, Numerus.PL),
    ),
    "beiden": GenusResolver(
        AllowedMorph(None, Kasus.DAT, Numerus.PL),
        AllowedMorph(None, Kasus.GEN, Numerus.PL),
    ),
    # I disable viel because the it is generally not inflected even though
    # the noun is accusative, like in viel Spaß
    # "viel": GR(
    #     AM(Genus.M, Kasus.NOM, Numerus.SG),
    #     AM(Genus.F, Kasus.NOM, Numerus.SG),
    #     AM(Genus.N, Kasus.NOM, Numerus.SG),
    #     AM(Genus.F, Kasus.ACC, Numerus.SG),
    #     AM(Genus.N, Kasus.ACC, Numerus.SG),
    # ),
    "vielen": GenusResolver(
        AllowedMorph(Genus.M, Kasus.ACC, Numerus.SG),
        AllowedMorph(Genus.M, Kasus.DAT, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.ACC, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.DAT, Numerus.SG),
        AllowedMorph(Genus.F, Kasus.DAT, Numerus.SG),
    ),
    # "viele",
    # "vieler",
    # "vieles",
    # "beides",
    # # "alles": GR(),
    # "alle": GR(),
    # "allem": GR(),
    # "allen": GR(),
    # "aller": GR(),
    # # "allerlei": GR(),
    # # "allermeisten": GR(),
    # #
    # "irgendein": GR(),
    # "wessen": GR(),
    # #
    # "etwas": GR(),
    # "was": GR(),
    # "irgendwas": GR(),
}

TERM_NONE = [
    "dein",
    "ein",
    "euer",
    "ihr",
    "kein",
    "mein",
    "sein",
    "unser",
    "dies",
    # "solch",
    # "mehr",
    # "wenig",
]

for term in TERM_NONE:
    RESOLVERS[term] = GenusResolver(
        AllowedMorph(Genus.M, Kasus.NOM, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.NOM, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.ACC, Numerus.SG),
    )


TERM_E = [
    #
    "diese",
    "eine",
    "irgendeine",
    "seine",
    "meine",
    "welche",
    # "solche",
    # "manche",
    "irgendwelche",
    "deine",
    "eure",
    "unsere",
    # "wenige",
    "keine",
    "einige",
    "jede",
    "ihre",
    "jegliche",
    # "mehrere",
    "meiste",
]

for term in TERM_E:
    RESOLVERS[term] = GenusResolver(
        AllowedMorph(Genus.F, Kasus.NOM, Numerus.SG),
        AllowedMorph(Genus.F, Kasus.ACC, Numerus.SG),
        AllowedMorph(None, Kasus.NOM, Numerus.PL),
        AllowedMorph(None, Kasus.ACC, Numerus.PL),
    )

TERM_S = [
    "eines",
    "eures",
    "einiges",
    "deines",
    "ihres",
    "dieses",
    "jedes",
    # "mehreres",
    "meines",
    "seines",
    "solches",
    "unseres",
    "welches",
    "fürs",
]

for term in TERM_S:
    RESOLVERS[term] = GenusResolver(
        AllowedMorph(Genus.M, Kasus.GEN, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.GEN, Numerus.SG),
    )

TERM_R = [
    "deiner",
    "dieser",
    "einer",
    "einiger",
    "eurer",
    "ihrer",
    "irgendeiner",
    "irgendwelcher",
    "jeder",
    "jeglicher",
    "jener",
    "keiner",
    "mancher",
    "meiner",
    "seiner",
    "solcher",
    "unserer",
    "welcher",
    "weniger",
]

for term in TERM_R:
    RESOLVERS[term] = GenusResolver(
        AllowedMorph(Genus.F, Kasus.DAT, Numerus.SG),
        AllowedMorph(Genus.F, Kasus.GEN, Numerus.SG),
        AllowedMorph(None, Kasus.GEN, Numerus.PL),
    )

TERM_M = [
    "deinem",
    "diesem",
    "einem",
    "eurem",
    "ihrem",
    "irgendeinem",
    "jedem",
    "jemandem",
    "jenem",
    "keinem",
    "meinem",
    "seinem",
    "solchem",
    "unserem",
    "welchem",
    "vom",
    "am",
    "im",
]

for term in TERM_M:
    RESOLVERS[term] = GenusResolver(
        AllowedMorph(Genus.M, Kasus.DAT, Numerus.SG),
        AllowedMorph(Genus.N, Kasus.DAT, Numerus.SG),
    )

TERM_N = [
    "diesen",
    "deinen",
    "einen",
    "einigen",
    "euren",
    "ihren",
    "irgendeinen",
    "jeden",
    "jeglichen",
    "jemanden",
    "keinen",
    "manchen",
    # "mehreren",
    "meinen",
    "meisten",
    "nen",
    "seinen",
    "solchen",
    "unseren",
    "welchen",
    # "wenigen",
    "wenigsten",
]

for term in TERM_N:
    RESOLVERS[term] = GenusResolver(
        AllowedMorph(Genus.M, Kasus.ACC, Numerus.SG),
        AllowedMorph(None, Kasus.DAT, Numerus.PL),
    )
