"""Pydantic schemas that form the contract between pipeline stages."""

from pydantic import BaseModel, Field


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="A list of web searches to perform to best answer the query."
    )


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


class ClarifyingQuestion(BaseModel):
    question: str = Field(
        description="A short question to put to the user, answerable in a sentence."
    )
    why: str = Field(description="Why the answer changes how the research should be done.")


class ClarificationPlan(BaseModel):
    questions: list[ClarifyingQuestion] = Field(
        description="The questions to ask before researching, most important first."
    )


class ClarifiedAnswer(BaseModel):
    """One question the user was asked, paired with what they said."""

    question: str
    answer: str
