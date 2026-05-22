import json
from functools import lru_cache


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_role: str = "routing-service"
    service_name: str = "routing_service"
    service_title: str = "Routing service"
    service_description: str = "Owns TrafficRoute state, route weights and Gateway API write requests."
    service_split_enabled: bool = True
    postgres_dsn: str = "postgresql://admin:admin@postgresql.hse-llm-project.svc.cluster.local:5432/default"
    security_audit_base_url: str = "http://security-audit-service.hse-llm-project.svc.cluster.local:8000"
    routing_service_url: str = "http://routing-service.hse-llm-project.svc.cluster.local:8000"
    validation_service_url: str = "http://validation-service.hse-llm-project.svc.cluster.local:8000"
    quota_service_url: str = "http://quota-service.hse-llm-project.svc.cluster.local:8000"
    cost_service_url: str = "http://cost-service.hse-llm-project.svc.cluster.local:8000"
    prometheus_base_url: str = "http://kube-prometheus-stack-prometheus.monitoring.svc.cluster.local:9090"
    service_to_service_urls_json: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def service_to_service_urls(self) -> dict[str, str]:
        if not self.service_to_service_urls_json.strip():
            return {}
        try:
            parsed = json.loads(self.service_to_service_urls_json)
        except json.JSONDecodeError:
            return {}
        return {str(k): str(v) for k, v in parsed.items()} if isinstance(parsed, dict) else {}


@lru_cache
def get_settings() -> Settings:
    return Settings()
