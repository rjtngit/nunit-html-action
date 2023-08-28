import sys
import os

from xml.dom.minidom import parse

from markyp_bootstrap4.alerts import alert
from markyp_bootstrap4.badges import span_badge
from markyp_html import webpage
from markyp_html.block import div, pre

from markyp_bootstrap4 import req
from markyp_bootstrap4.layout import container, one
from markyp_html.inline import span, br
from markyp_html.text import h3, p, h6


def html_summary(test_results):
    summary = test_results["summary"]
    return div(
        alert.info(
            h3("Summary"),
            span_badge.info(f"Tests: {summary['total']}"),
            span_badge.danger(f"Failed: {summary['failed']}"),
            span_badge.success(f"Passed: {summary['passed']}"),
            span_badge.secondary(f"Inconclusive: {summary['inconclusive']}"),
            span_badge.secondary(f"Skipped: {summary['skipped']}"),
            span_badge.light(f"Date: {summary['date']}"),
            span_badge.light(f"Duration: {summary['duration']}"),
        ),
        style="margin-top: 1rem;"
    )


def html_test_row_content(test):
    return div(
        h3(test["name"], style="overflow-wrap: break-word;"),
        (span_badge.danger(f"{test['result']}") if len(test['message']) > 0 else span_badge.light(f"{test['result']}")),
        span_badge.light(f"Duration: {test['duration']}"),
        p(),
        span(span(h6(f"Message"), p(f"{test['message']}")) if len(test['message']) > 0 else ""),
        span(span(h6(f"Stack Trace"), pre(f"{test['stack-trace']}", class_="bg-white")) if len(test['stack-trace']) > 0 else ""),
    )


def html_test_row(test):
    if test["result"] == "Failed":
        return alert.danger(html_test_row_content(test))
    if test["result"] == "Passed":
        return alert.success(html_test_row_content(test))
    return alert.secondary(html_test_row_content(test))


def html_test_list(test_results):
    tests = test_results["tests"]
    return div(
        *(html_test_row(item) for index, item in enumerate(tests)),
    )


def html_container(test_results):
    return div(
        html_summary(test_results),
        html_test_list(test_results)
    )


def make_html(test_results):
    page = webpage(
        container(
            one(
                html_container(test_results),
            )
        ),
        page_title="Test Results",
        head_elements=[
            req.bootstrap_css,
            *req.all_js
        ]
    )
    return str(page)


def get_element_value(child, tag):
    try:
        return child.getElementsByTagName(tag)[0].firstChild.nodeValue
    except:
        return ""


def parse_xml(filename_xml):
    xml = parse(filename_xml)
    results = {
        "summary": {},
        "tests": [],
    }
    # Parse summary
    xml_summary = xml.getElementsByTagName("test-run")[0]
    results["summary"]["total"] = xml_summary.getAttribute("total")
    results["summary"]["passed"] = xml_summary.getAttribute("passed")
    results["summary"]["failed"] = xml_summary.getAttribute("failed")
    results["summary"]["inconclusive"] = xml_summary.getAttribute("inconclusive")
    results["summary"]["skipped"] = xml_summary.getAttribute("skipped")
    results["summary"]["asserts"] = xml_summary.getAttribute("asserts")
    results["summary"]["date"] = xml_summary.getAttribute("start-time")
    results["summary"]["duration"] = xml_summary.getAttribute("duration")
    # Parse tests
    for child in xml.getElementsByTagName("test-case"):
        results["tests"].append({
            "name": child.getAttribute("fullname"),
            "result": child.getAttribute("result"),
            "duration": child.getAttribute("duration"),
            "message": get_element_value(child, "message"),
            "stack-trace": get_element_value(child, "stack-trace"),
        })
    # Bring failures to top
    for i, item in enumerate(results["tests"]):
        if item["result"] == "Failed":
            results["tests"].insert(0, results["tests"].pop(i))
    return results


def main():
    if len(sys.argv) < 2:
        print("Error: Missing XML input file path")
        sys.exit(1)
    filename_xml = sys.argv[1]
    filename_html = filename_xml.replace(".xml", "") + ".html"
    if len(sys.argv) > 2:
        filename_html = sys.argv[2]
    test_results = parse_xml(filename_xml)
    html = make_html(test_results)
    os.makedirs(os.path.dirname(filename_html), exist_ok=True)
    file = open(filename_html, "w")
    file.write(html)
    file.close()


if __name__ == "__main__":
    main()
