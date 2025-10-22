from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.knowledge_config import KnowledgeConfig

from utils import TRAVEL_DIR, TI_VPN_DIR


@CrewBase
class SystemExperts:
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def router_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["router_manager"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def travel_requests_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["travel_requests_specialist"],  # type: ignore[index]
            verbose=True,
            knowledge_config=KnowledgeConfig(results_limit=8, score_threshold=0.45),
        )

    @agent
    def it_vpn_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["it_vpn_specialist"],  # type: ignore[index]
            verbose=True,
            knowledge_config=KnowledgeConfig(results_limit=8, score_threshold=0.45),
        )

    @task
    def router_task(self) -> Task:
        return Task(
            config=self.tasks_config["router_task"],  # type: ignore[index]
        )

    @task
    def air_ticket_flow_task(self) -> Task:
        return Task(
            config=self.tasks_config["air_ticket_flow_task"],  # type: ignore[index]
            output_file="guia_passagem_aerea.md",
        )

    @task
    def accommodation_flow_task(self) -> Task:
        return Task(
            config=self.tasks_config["accommodation_flow_task"],  # type: ignore[index]
            output_file="guia_hospedagem.md",
        )

    @task
    def vpn_access_ticket_flow_task(self) -> Task:
        return Task(
            config=self.tasks_config["vpn_access_ticket_flow_task"],  # type: ignore[index]
            output_file="guia_vpn.md",
        )

    @crew
    def crew(self) -> Crew:
        travel_flow_file = TRAVEL_DIR / "sgv_fluxo_basico.txt"
        it_flow_file = TI_VPN_DIR / "vpn_fluxo_basico.txt"
        return Crew(
            agents=self.agents,
            manager_llm="gpt-4.1",
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            knowledge_sources=[
                TextFileKnowledgeSource(file_paths=[travel_flow_file, it_flow_file])
            ],
        )
