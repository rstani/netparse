import logging
import os
import re
from functools import lru_cache

import textfsm
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.html import escape

#from dotenv import load_dotenv
from genie.conf.base import Device  # Import the Device class
from genie.libs.parser.utils import get_parser

# Load environment variables
#load_dotenv()

# Configure a basic logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Get environment variables for directories
TEXTFSM_DIR = os.getenv(
    "TEXTFSM_DIR",
    "/usr/src/app/src/netparse/parser_app/parser_templates/ntc-templates/ntc_templates/templates",
)
GENIE_PARSER_ROOT = os.getenv(
    "GENIE_PARSER_ROOT", "/usr/local/lib/python3.12/site-packages/genie/libs/parser"
)


# Function to get all parsers and unify them
@lru_cache(maxsize=1)
def get_all_parsers():
    parsers = {}
    parsers.update(get_textfsm_parsers())
    parsers.update(get_genie_parsers())
    return parsers


# Function to get all TextFSM parsers
def get_textfsm_parsers():
    textfsm_parsers = {}
    for f in os.listdir(TEXTFSM_DIR):
        if f.endswith(".textfsm") and os.path.isfile(os.path.join(TEXTFSM_DIR, f)):
            command_name = f.replace(".textfsm", "")
            parts = command_name.split("_")
            if len(parts) > 1:
                os_name = parts[0].lower()
                command_part = "_".join(parts[1:])
            else:
                os_name = "generic"
                command_part = command_name
            parser_key = f"Textfsm_{os_name}_{command_part}"
            textfsm_parsers[parser_key] = {
                "type": "textfsm",
                "filename": f,
            }
    return textfsm_parsers


# Function to get all Genie parsers
def get_genie_parsers():
    genie_parsers = {}
    for root, dirs, files in os.walk(GENIE_PARSER_ROOT):
        platform_match = re.search(r"parser[\\/](\w+)", root)
        if platform_match:
            platform = platform_match.group(1).lower()
        else:
            continue

        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                command_name = file.replace(".py", "")
                if (
                    command_name.startswith("show_")
                    and "golden_output" not in command_name
                ):
                    command_name_with_spaces = command_name.replace("_", " ")
                    parser_key = f"Genie_{platform}_{command_name}"
                    genie_parsers[parser_key] = {
                        "type": "genie",
                        "platform": platform,
                        "command": command_name_with_spaces,
                        "filename": file,
                    }
    return genie_parsers


# Function to handle TextFSM parsing
def parse_textfsm(raw_output, parser_info):
    template_path = os.path.join(TEXTFSM_DIR, parser_info["filename"])
    with open(template_path) as template_file:
        fsm = textfsm.TextFSM(template_file)
        parsed_output = fsm.ParseText(raw_output)
    return parsed_output


# Function to handle Genie parsing
def parse_genie(raw_output, parser_info):
    device = Device(name="mock_device", os=parser_info["platform"])
    parsed_output = device.parse(parser_info["command"], output=raw_output)
    return parsed_output


# View for the main page
def index(request):
    parsers = get_all_parsers()
    return render(request, "parser_app/index.html", {"parsers": parsers.keys()})


# View to handle parsing
def parse_command(request):
    if request.method == "POST":
        raw_output = request.POST.get("raw_output")
        parser_choice = request.POST.get("parser_choice")

        if not raw_output or not parser_choice:
            return JsonResponse({"error": "Invalid input"}, status=400)

        parsers = get_all_parsers()
        parser_info = parsers.get(parser_choice)

        if not parser_info:
            return JsonResponse({"error": "Parser not found"}, status=404)

        try:
            if parser_info["type"] == "textfsm":
                parsed_output = parse_textfsm(raw_output, parser_info)
            elif parser_info["type"] == "genie":
                parsed_output = parse_genie(raw_output, parser_info)
            else:
                return JsonResponse({"error": "Unknown parser type"}, status=400)

            return JsonResponse({"parsed_output": parsed_output}, safe=False)

        except FileNotFoundError:
            logger.error(f"Parser template not found: {parser_choice}")
            return JsonResponse({"error": "Parser template not found"}, status=404)
        except Exception as e:
            logger.exception("Unexpected error occurred during parsing")
            return JsonResponse({"error": "Unexpected error occurred"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
