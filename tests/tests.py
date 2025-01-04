from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse


class ParseCommandTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.parse_url = reverse("parse_command")

        # Sample mock data
        self.raw_output = "Mock raw device output"
        self.parser_choice = "Textfsm_ios_show_version"
        self.mock_parsers = {
            "Textfsm_ios_show_version": {
                "type": "textfsm",
                "filename": "ios_show_version.textfsm",
            },
            "Genie_ios_show_version": {
                "type": "genie",
                "platform": "ios",
                "command": "show version",
                "filename": "show_version.py",
            },
        }

    @patch("parser_app.views.get_all_parsers", return_value=mock_parsers)
    @patch("parser_app.views.parse_textfsm", return_value=[["Parsed Output"]])
    def test_parse_command_textfsm_success(
        self, mock_parse_textfsm, mock_get_all_parsers
    ):
        response = self.client.post(
            self.parse_url,
            {"raw_output": self.raw_output, "parser_choice": self.parser_choice},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("parsed_output", response.json())

    @patch("parser_app.views.get_all_parsers", return_value=mock_parsers)
    def test_parse_command_parser_not_found(self, mock_get_all_parsers):
        response = self.client.post(
            self.parse_url,
            {"raw_output": self.raw_output, "parser_choice": "InvalidParser"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())

    def test_parse_command_invalid_input(self):
        response = self.client.post(
            self.parse_url, {"raw_output": "", "parser_choice": ""}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
