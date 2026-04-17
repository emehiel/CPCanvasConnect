import os, collections
import pytest as pt
from CPCanvasConnect import groups

class TestGroups:
    @pt.fixture
    def group_id(self):
        # Group Alpha: 233747
        # Group Beta: 233748
        return os.getenv("ALPHA_GROUP_ID", None)

    @pt.fixture
    def user_id(self):
        return os.getenv("TEST_USER_ID", None)
    
    @pt.fixture
    def assignment_id(self):
        # Peer Review Assignment in emehiel sand-box: 1417904
        return int(os.getenv("TEST_ASSIGNMENT_ID", None))
    
    @pt.fixture
    def canvas_client(self):
        canvas_client = groups.get_canvas_client()
        return canvas_client
    
    @pt.fixture
    def course_id(self):
        # emehiel sand-box course id: 15224
        return int(os.getenv("TEST_COURSE_ID", None))
    
    @pt.fixture
    def course(self, canvas_client, course_id):
        canvas_client = groups.get_canvas_client()
        return canvas_client.get_course(course_id)
    
    @pt.fixture
    def known_members(self):
        return [15749, 85705, 30909, 110456]
    
    @pt.fixture
    def known_groups(self):
        return ["Alpha", "Beta"]
    
    def test_get_canvas_client(self):
        client = groups.get_canvas_client()
        assert isinstance(client, groups.Canvas)

    def test_get_group_members(self, canvas_client, course, group_id, known_members):
        members = groups.get_group_members(canvas_client, group_id)
        assert isinstance(members, list)
        assert len(members) > 0
        assert  collections.Counter([m["id"] for m in members]) == collections.Counter(known_members)

    def test_assign_group_peer_reviews(self, canvas_client, course_id, assignment_id, group_id):
        groups.assign_group_peer_reviews(canvas_client, course_id, assignment_id, group_id)
        # If no exceptions were raised, we assume success for this test.
        assert True

    def test_list_course_groups(self, canvas_client, course_id, known_groups):
        course_groups = groups.list_course_groups(canvas_client, course_id)
        assert isinstance(course_groups, list)
        assert len(course_groups) > 0
        assert collections.Counter([g["name"] for g in course_groups]) == collections.Counter(known_groups)

    def test_get_course_group_ids(self, canvas_client, course_id, known_groups):
        group_ids = groups.get_course_group_ids(canvas_client, course_id)
        assert isinstance(group_ids, list)
        assert len(group_ids) == len(known_groups)