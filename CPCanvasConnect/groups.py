from canvasapi import Canvas
from typing import List, Iterable
import os

def get_canvas_client(api_url: str = None, api_key: str = None) -> Canvas:
    """Return a Canvas client object.

    Looks for values in the environment if not supplied explicitly:
      CANVAS_API_URL and CANVAS_API_KEY
    """
    api_url = api_url or os.environ.get("CANVAS_API_URL")
    api_url = api_url or os.getenv("CANVAS_API_URL")
    api_key = api_key or os.environ.get("CANVAS_API_KEY")

    if not api_url or not api_key:
        raise ValueError("Canvas API URL and API key must be provided via args or CANVAS_API_URL/CANVAS_API_KEY env vars")
    
    return Canvas(api_url, api_key)

def get_group_members(canvasClient: Canvas, group_id: int) -> List[dict]:
    """Return a list of member dictionaries for the provided group id.

    Uses the group.get_users() call from canvasapi and converts results
    into plain dicts (id, name, sortable_name, email when available) to make
    the function easy to test and inspect.
    """
    group = canvasClient.get_group(group_id)
    members = []
    for user in group.get_users():
        # Some user objects returned by canvasapi are objects; cast to dict safely
        member = {
            "id": getattr(user, "id", None),
            "name": getattr(user, "name", None),
            "sortable_name": getattr(user, "sortable_name", None),
            "email": getattr(user, "login_id", None),
            "sis_user_id": getattr(user, "sis_user_id", None),
        }
        members.append(member)
    return members

def assign_group_peer_reviews(client: Canvas, course_id: int, assignment_id: int, group_id: int) -> None:
    """Assign peer reviews among members of a given group for a specific assignment."""
    group_members = get_group_members(client, group_id)

    course = client.get_course(course_id)
    assignment = course.get_assignment(assignment_id)

    for reviewer in group_members:
        for reviewee in group_members:
            if reviewer["id"] != reviewee["id"]:
                submission = assignment.get_submission(reviewer["id"])
                submission.create_submission_peer_review(reviewee["id"])

def list_course_groups(canvas: Canvas, course_id: int) -> Iterable:
    """Yield groups for a given course id."""
    course = canvas.get_course(course_id)
    yield from course.get_groups()

def get_course_group_ids(canvas: Canvas, course_id: int) -> List[int]:
    """Return a list of group ids for the given course."""
    ids: List[int] = []
    course = canvas.get_course(course_id)
    for g in course.get_groups():
        gid = getattr(g, "id", None)
        if gid is not None:
            ids.append(int(gid))
    return ids