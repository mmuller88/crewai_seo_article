import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai_seo_article.tools.custom_tool import MyCustomTool
# from crewai_seo_article.tools.serper_dev_tool import SerperDevTool
from crewai_tools import SerperDevTool
from crewai_seo_article.tools.long_tail_keyword_tool import LongTailKeywordTool

from dotenv import load_dotenv
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

load_dotenv()


@CrewBase
class CrewaiSeoArticle():
    """CrewaiSeoArticle crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Create a text file knowledge source
    text_source = TextFileKnowledgeSource(
        file_paths=["article_content_writer_temperatur_empfehlung.md"]
    )

    @agent
    def article_content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['article_content_writer'],
            verbose=True,
            # knowledge_sources=[self.text_source]
        )

    @agent
    def also_asked_researcher(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config['also_asked_researcher'],
            verbose=True,
            tools=[search_tool],
            # knowledge_sources=[self.text_source]
        )
    
    @agent
    def also_asked_answerer(self) -> Agent:
        return Agent(
            config=self.agents_config['also_asked_answerer'],
            verbose=True,
            # knowledge_sources=[self.text_source]
        )

    @task
    def article_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['article_content_task'],
            tools=[LongTailKeywordTool()]
        )

    @task
    def also_asked_task(self) -> Task:
        return Task(
            config=self.tasks_config['also_asked_task']
        )

    @task
    def also_asked_answerer_task(self) -> Task:
        return Task(
            config=self.tasks_config['also_asked_answerer_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiSeoArticle crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            # memory=True,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
