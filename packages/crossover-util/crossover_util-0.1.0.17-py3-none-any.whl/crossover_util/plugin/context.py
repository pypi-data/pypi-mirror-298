from typing import Dict, List

from pydantic import BaseModel, Field


class PluginContext(BaseModel):
    environment: Dict[str, str] = Field(default_factory=dict)
    args: List[str] = Field(default_factory=list)

    @property
    def env_str(self) -> str:
        return " ".join([f"{k}={v}" for k, v in self.environment.items()])

    @property
    def args_str(self) -> str:
        return " ".join(self.args)
