from typing import Any, Optional
from pydantic import BaseModel, field_validator
import datetime as dt
from .events import dbtEvent


class NodeState(BaseModel):
    materialized: str
    meta: dict[str, Any]
    node_finished_at: Optional[dt.datetime] = None
    node_name: str
    node_path: str
    node_relation: dict[str, Any]
    node_started_at: dt.datetime
    node_status: str
    resource_type: str
    unique_id: str

    @field_validator('node_finished_at', mode='before')
    @classmethod
    def blank_node_finished_at(cls, v: str):
        if v == '':
            return None
        return v

    def duration(self):
        if not self.node_finished_at:
            return dt.datetime.utcnow() - self.node_started_at
        else:
            return self.node_finished_at - self.node_started_at

class RunState:
    def __init__(self, events: list[dbtEvent]):
        self.events = events
        self.finished = False
        self.run_started_at = None
        self.invocation_id = None
        self.dbt_version = None
        self.dbt_log_version = None
        self.node_count = None
        self.num_threads = None
        self.target_name = None
        self.adapter_name = None
        self.adapter_version = None
        self.nodes: dict[str, NodeState] = dict()

    def add_event(self, event: dbtEvent):
        self.events.append(event)

    def update_node(self, node: NodeState):
        self.nodes[node.unique_id] = node

    def nodes_with_status(self, status: str):
        return [n for n in self.nodes.values() if n.node_status == status]

    def finished_nodes(self):
        return [n for n in self.nodes.values() if n.node_status != 'started']

    def finished_node_count(self):
        return len(self.finished_nodes())
