import pytest
from src.discord_mcp.client import _validate_discord_id


class TestValidateDiscordId:
    """Tests for Discord snowflake ID validation."""

    def test_valid_numeric_id(self):
        assert (
            _validate_discord_id("1353689257796960296", "server_id")
            == "1353689257796960296"
        )

    def test_valid_short_id(self):
        assert _validate_discord_id("1", "server_id") == "1"

    def test_valid_max_length_id(self):
        assert (
            _validate_discord_id("12345678901234567890", "server_id")
            == "12345678901234567890"
        )

    def test_rejects_empty_string(self):
        with pytest.raises(ValueError, match="Invalid server_id"):
            _validate_discord_id("", "server_id")

    def test_rejects_non_numeric(self):
        with pytest.raises(ValueError, match="Invalid channel_id"):
            _validate_discord_id("abc123", "channel_id")

    def test_rejects_path_traversal(self):
        with pytest.raises(ValueError, match="Invalid guild_id"):
            _validate_discord_id("../../etc/passwd", "guild_id")

    def test_rejects_js_injection(self):
        with pytest.raises(ValueError, match="Invalid server_id"):
            _validate_discord_id("123;alert(1)", "server_id")

    def test_rejects_spaces(self):
        with pytest.raises(ValueError, match="Invalid server_id"):
            _validate_discord_id("123 456", "server_id")

    def test_rejects_negative(self):
        with pytest.raises(ValueError, match="Invalid server_id"):
            _validate_discord_id("-1", "server_id")

    def test_rejects_too_long(self):
        with pytest.raises(ValueError, match="Invalid server_id"):
            _validate_discord_id("123456789012345678901", "server_id")

    def test_name_appears_in_error(self):
        with pytest.raises(ValueError, match="Invalid my_field"):
            _validate_discord_id("not-a-number", "my_field")
