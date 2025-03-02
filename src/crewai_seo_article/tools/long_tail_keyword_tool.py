from typing import Any, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from .serper_dev_tool import SerperDevTool


class LongTailKeywordSchema(BaseModel):
    """Input for LongTailKeywordTool."""
    keyword: str = Field(
        ...,
        description="The main keyword to find long-tail keyword variations for"
    )


class LongTailKeywordTool(BaseTool):
    name: str = "Find Long-tail Keywords"
    description: str = (
        "A tool that finds long-tail keyword variations for a given keyword "
        "by analyzing related searches and questions people ask"
    )
    args_schema: Type[BaseModel] = LongTailKeywordSchema
    serper_tool: SerperDevTool = None

    def __init__(self):
        super().__init__()
        self.serper_tool = SerperDevTool(
            country="de",
            locale="de",
        )

    def _extract_long_tail_keywords(self, results: dict) -> dict:
        """Extract and categorize long-tail keywords from search results."""
        long_tail_keywords = {
            "questions": [],
            "related_searches": [],
            "combined_suggestions": []
        }

        # Extract questions from "People Also Ask"
        if "peopleAlsoAsk" in results:
            questions = [item["question"] for item in results["peopleAlsoAsk"]]
            long_tail_keywords["questions"] = questions
            long_tail_keywords["combined_suggestions"].extend(questions)

        # Extract related searches
        if "relatedSearches" in results:
            related = [item["query"] for item in results["relatedSearches"]]
            long_tail_keywords["related_searches"] = related
            long_tail_keywords["combined_suggestions"].extend(related)

        return long_tail_keywords

    def _run(self, **kwargs: Any) -> Any:
        """Execute the long-tail keyword search operation."""
        keyword = kwargs.get("keyword")

        # Get search results using SerperDevTool
        search_results = self.serper_tool._run(
            search_query=keyword,
            search_type="search"
        )

        # Extract and process long-tail keywords
        long_tail_results = self._extract_long_tail_keywords(search_results)

        return {
            "original_keyword": keyword,
            "long_tail_keywords": long_tail_results
        }
