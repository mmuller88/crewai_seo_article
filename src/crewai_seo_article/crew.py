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

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    # @agent
    # def researcher(self) -> Agent:
    # 	return Agent(
    # 		config=self.agents_config['researcher'],
    # 		verbose=True
    # 	)

    # @agent
    # def reporting_analyst(self) -> Agent:
    # 	return Agent(
    # 		config=self.agents_config['reporting_analyst'],
    # 		verbose=True
    # 	)

    @agent
    def article_content_writer(self) -> Agent:

        return Agent(
            role="Produktbeschreiber",
            goal="Erstelle präzise und ansprechende Produktbeschreibungen, die alle wichtigen Eigenschaften des Kleidungsstücks verständlich vermitteln.",
            backstory="Sie sind ein erfahrener Texter im Bereich Mode und Textilien mit einem ausgeprägten Gespür für Materialien und Verarbeitung. Bekannt für Ihre Fähigkeit, technische Eigenschaften in verständliche und ansprechende Produktbeschreibungen zu übersetzen, die sowohl informativ als auch verkaufsfördernd sind.",
            # config=self.agents_config['article_content_writer'],
            verbose=True,
            # tools=[search_tool],
            knowledge_sources=[self.text_source]
        )

    @agent
    def also_asked_researcher(self) -> Agent:
        search_tool = SerperDevTool()

        return Agent(
            role="Auch gefragt Fragebauer",
            goal="Finde heraus, welche Fragen die Nutzer häufiger stellen und welche Themen sie interessieren.",
            # config=self.agents_config['article_content_writer'],
            backstory="Sie sind ein erfahrener Fragebauer und haben ein großes Interesse an den Bedürfnissen und Wünschen der Nutzer. Sie sind ein Experte für das Finden von Informationen und haben ein gutes Gespür für die Bedürfnisse der Nutzer.",
            verbose=True,
            tools=[search_tool],
            knowledge_sources=[self.text_source]
        )
    
    @agent
    def also_asked_answerer(self) -> Agent:

        return Agent(
            role="Auch gefragt Antworter",
            goal="Antworte auf die Fragen, die die Nutzer häufiger stellen.",
            # config=self.agents_config['article_content_writer'],
            backstory="Sie sind ein erfahrener Antworter und haben ein großes Interesse an den Bedürfnissen und Wünschen der Nutzer. Sie sind ein Experte für das Finden von Informationen und haben ein gutes Gespür für die Bedürfnisse der Nutzer.",
            verbose=True,
            knowledge_sources=[self.text_source]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    # @task
    # def research_task(self) -> Task:
    # 	return Task(
    # 		config=self.tasks_config['research_task'],
    # 	)

    # @task
    # def reporting_task(self) -> Task:
    # 	return Task(
    # 		config=self.tasks_config['reporting_task'],
    # 		output_file='report.md'
    # 	)

    @task
    def article_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['article_content_task'],
            tools=[LongTailKeywordTool()]
        )

    @task
    def also_asked_task(self) -> Task:
        return Task(
            config={
                'description': "Finde die fünf häufigsten Fragen heraus, welche die Nutzer stellen und welche Themen sie interessieren im Zusammenhang mit dem Produkt.",
                'expected_output': "Eine Liste von Fragen und Themen, die die Nutzer häufiger stellen und interessieren.",
                'agent': self.also_asked_researcher()
            }
        )

    @task
    def also_asked_answerer_task(self) -> Task:
        return Task(
            config={
                'description': "Antworte auf die Fragen, die die Nutzer häufiger stellen.",
                'expected_output': "Eine Liste von Fragen und Antworten.",
                'agent': self.also_asked_answerer()
            }
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
            memory=True,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
