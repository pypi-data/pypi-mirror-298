from typing import TypeVar, Optional
from ai_haley_kg_domain.model.KGNode import KGNode
from vital_ai_vitalsigns.model.GraphObject import GraphObject
from kgraphservice.kgraph_service_inf import KGraphServiceInterface
from kgraphservice.part.kgframe_part import KGFramePart

G = TypeVar('G', bound=Optional[GraphObject])
KGN = TypeVar('KGN', bound=Optional[KGNode])
KGFP = TypeVar('KGFP', bound=Optional[KGFramePart])


class KGraphServiceREST(KGraphServiceInterface):
    pass

# use client to connect to rest implementation

