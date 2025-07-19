from pprint import pprint

from langchain_core.messages import HumanMessage
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from src.config import get_large_model, get_small_model
from src.prompt import SOCRATES_BUDDY_PROMPT
from src.socrates import get_today_sessions
from collections import defaultdict


def get_up_to_date_schedule() -> str:
    """
    Return the schedule for today.
    """
    sessions = get_today_sessions()

    # Group sessions by time
    sessions_by_time = defaultdict(list)
    for session in sessions:
        time = session["time"]
        sessions_by_time[time].append(session)

    # Sort times
    sorted_times = sorted(
        sessions_by_time.keys(),
        key=lambda x: x if x not in ["any time", "till Sunday afternoon"] else "zz:zz",
    )

    # Format the schedule
    schedule_lines = []
    schedule_lines.append("📅 SoCraTes Schedule")
    schedule_lines.append("=" * 50)

    for time in sorted_times:
        sessions_at_time = sessions_by_time[time]

        # Add time header
        schedule_lines.append(f"\n🕐 {time}")
        schedule_lines.append("-" * 20)

        # Sort sessions by room for consistent ordering
        sessions_at_time.sort(key=lambda x: x["room"])

        for session in sessions_at_time:
            room = session["room"]
            title = session["title"] or "TBD"
            owner = session["session_owner"]

            # Format each session
            schedule_lines.append(f"  📍 {room}")
            schedule_lines.append(f"     {title}")
            schedule_lines.append(f"     by {owner}")
            schedule_lines.append("")

    return "\n".join(schedule_lines)


class Session(BaseModel):
    title: str
    time: str
    room: str
    owner: str


def save_schedule(schedule: list[Session]) -> str:
    """
    Save the schedule to a markdown file.
    """
    markdown_lines = []
    markdown_lines.append("# SoCraTes Schedule")
    markdown_lines.append("")

    # Group sessions by time
    sessions_by_time = {}
    for session in schedule:
        time = session.time
        if time not in sessions_by_time:
            sessions_by_time[time] = []
        sessions_by_time[time].append(session)

    # Sort times
    sorted_times = sorted(sessions_by_time.keys())

    for time in sorted_times:
        markdown_lines.append(f"## {time}")
        markdown_lines.append("")

        sessions_at_time = sessions_by_time[time]
        sessions_at_time.sort(key=lambda x: x.room)

        for session in sessions_at_time:
            markdown_lines.append(f"**{session.title}**")
            markdown_lines.append(f"- 📍 Room: {session.room}")
            markdown_lines.append(f"- 👤 Owner: {session.owner}")
            markdown_lines.append("")

    markdown_content = "\n".join(markdown_lines)

    with open("schedule.md", "w") as f:
        f.write(markdown_content)
    return "Schedule saved to schedule.md"


socrates_buddy = create_react_agent(
    model=get_large_model(),
    tools=[get_up_to_date_schedule],
    prompt=SOCRATES_BUDDY_PROMPT,
)

if __name__ == "__main__":
    output = socrates_buddy.invoke(
        MessagesState(messages=[HumanMessage("What is the schedule for today?")]),
    )
    print(output)
