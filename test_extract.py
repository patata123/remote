import pytest
from unittest.mock import MagicMock
from extract import format_sender


def make_user(first=None, last=None, username=None, uid=123):
    from telethon.tl.types import User
    u = MagicMock(spec=User)
    u.first_name = first
    u.last_name = last
    u.username = username
    u.id = uid
    return u


def make_channel(title=None, uid=456):
    from telethon.tl.types import Channel
    c = MagicMock(spec=Channel)
    c.title = title
    c.id = uid
    return c


class TestFormatSender:
    def test_none_returns_unknown(self):
        assert format_sender(None) == "Unknown"

    def test_user_full_name(self):
        assert format_sender(make_user(first="Alice", last="Tan")) == "Alice Tan"

    def test_user_first_name_only(self):
        assert format_sender(make_user(first="Bob")) == "Bob"

    def test_user_falls_back_to_username(self):
        assert format_sender(make_user(username="charlie99")) == "charlie99"

    def test_user_falls_back_to_id(self):
        assert format_sender(make_user(uid=999)) == "999"

    def test_channel_with_title(self):
        assert format_sender(make_channel(title="Badminton SG")) == "Badminton SG"

    def test_channel_no_title_returns_id(self):
        assert format_sender(make_channel(title=None, uid=456)) == "456"


class TestSafeFilename:
    """Tests for the safe-name logic inlined in main()."""

    def _safe(self, name):
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)

    def test_alphanumeric_unchanged(self):
        assert self._safe("BadmintonSG") == "BadmintonSG"

    def test_spaces_replaced(self):
        assert self._safe("Badminton SG") == "Badminton_SG"

    def test_special_chars_replaced(self):
        assert self._safe("Chat/Group!") == "Chat_Group_"

    def test_hyphens_and_underscores_kept(self):
        assert self._safe("my-chat_group") == "my-chat_group"
