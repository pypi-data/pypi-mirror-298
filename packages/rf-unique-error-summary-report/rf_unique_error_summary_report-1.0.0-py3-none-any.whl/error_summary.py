import xml.etree.ElementTree as ET
from collections import defaultdict
import html
import re
import argparse


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


def extract_failure_messages(root):
    errors = defaultdict(lambda: {"count": 0, "latest_test": ""})

    for testcase in root.findall(".//testcase"):
        test_name = testcase.get("name")
        failure = testcase.find("failure")
        if failure is not None:
            message = failure.get("message")
            if message:
                match = re.search(
                    r"New message:</span>\s*(.*?)<br>", message, re.DOTALL
                )
                if match:
                    message = match.group(1).strip()
                    message = re.sub(r"<[^>]+>", "", message)
                    if message.startswith("FAILURE: "):
                        message = message[len("FAILURE: ") :]
                errors[message]["count"] += 1
                errors[message]["latest_test"] = test_name

    return errors


def generate_html(errors, output_file):
    html_content = """
    <html>
    <head>
        <title>Test Failures</title>
    </head>
    <body>
        <table border="1">
            <tr>
                <th>Error</th>
                <th>Count</th>
                <th>Latest Test Name</th>
            </tr>
    """

    for error, details in errors.items():
        html_content += f"""
            <tr>
                <td>
                    {html.escape(error)}
                </td>
                <td>{details['count']}</td>
                <td>{html.escape(details['latest_test'])}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(output_file, "w") as file:
        file.write(html_content)


def main():
    parser = argparse.ArgumentParser(description="Process an XML file.")
    parser.add_argument("input_file", type=str, help="Path to the XML file")
    parser.add_argument("output_file", type=str, help="Path to the output HTML file")
    args = parser.parse_args()

    root = parse_xml(args.input_file)
    errors = extract_failure_messages(root)
    generate_html(errors, args.output_file)


if __name__ == "__main__":
    main()
