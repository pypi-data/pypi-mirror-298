import pandas as pd
import plotly.express as px
import xml.etree.ElementTree as ET
import plotly.io as pio
import sys


# Function to parse JUnit XML file
def parse_junit_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    test_cases = []

    for testcase in root.iter("testcase"):
        test_case_data = {
            "classname": testcase.attrib.get("classname"),
            "name": testcase.attrib.get("name"),
            "time": float(testcase.attrib.get("time", 0)),
            "status": "passed",
        }

        for child in testcase:
            if child.tag == "failure":
                test_case_data["status"] = "failed"
                test_case_data["message"] = child.attrib.get("message")

        test_cases.append(test_case_data)

    return pd.DataFrame(test_cases)


def main():
    if len(sys.argv) != 2:
        print("Usage: run_dashboard <path_to_junit_xml>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Parse the JUnit XML file
    df = parse_junit_xml(file_path)

    # 1. Pie chart showing passed/failed percentage with count
    status_summary = df["status"].value_counts().reset_index()
    status_summary.columns = ["status", "count"]
    fig_status_pie = px.pie(
        status_summary, names="status", values="count", title="Test Cases by Status"
    )
    fig_status_pie.update_layout(
        title_font=dict(size=24, family="Arial, sans-serif", color="black"),
        title_font_weight="bold",
        showlegend=True,
        legend_title_text="Status",
        legend=dict(font=dict(size=12, color="black")),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    # 2. Bar chart showing top 10 failures with occurrence count
    failed_tests = df[df["status"] == "failed"]
    failure_counts = failed_tests["name"].value_counts().reset_index().head(10)
    failure_counts.columns = ["test_name", "count"]
    fig_top_failures = px.bar(
        failure_counts,
        x="test_name",
        y="count",
        title="Top 10 Failures by Occurrence Count",
    )
    fig_top_failures.update_layout(
        title_font=dict(size=24, family="Arial, sans-serif", color="black"),
        title_font_weight="bold",
        xaxis_title="Test Name",
        yaxis_title="Count",
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    # 3. Bar chart grouping failures by suite name and showing top 10 suites with most failures
    failed_suites = failed_tests["classname"].value_counts().reset_index().head(10)
    failed_suites.columns = ["suite_name", "count"]
    fig_failed_suites = px.bar(
        failed_suites,
        x="suite_name",
        y="count",
        title="Top 10 Suites with Most Failures",
    )
    fig_failed_suites.update_layout(
        title_font=dict(size=24, family="Arial, sans-serif", color="black"),
        title_font_weight="bold",
        xaxis_title="Suite Name",
        yaxis_title="Count",
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    # 4. Bar chart of top 10 slow tests (execution time in descending order)
    slow_tests = df.sort_values(by="time", ascending=False).head(10)
    fig_slow_tests = px.bar(
        slow_tests, x="name", y="time", title="Top 10 Slow Tests by Execution Time"
    )
    fig_slow_tests.update_layout(
        title_font=dict(size=24, family="Arial, sans-serif", color="black"),
        title_font_weight="bold",
        xaxis_title="Test Name",
        yaxis_title="Time (s)",
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    # Combine the charts into a single dashboard HTML file
    with open("dashboard.html", "w", encoding="utf-8") as dashboard:
        dashboard.write(
            """
            <html>
            <head>
                <title>RF Quick Dashboard</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f4;
                    }
                    .container {
                        width: 80%;
                        margin: auto;
                        overflow: hidden;
                    }
                    header {
                        background: #50b3a2;
                        color: #fff;
                        padding-top: 30px;
                        min-height: 70px;
                        border-bottom: #e8491d 3px solid;
                    }
                    header a {
                        color: #fff;
                        text-decoration: none;
                        text-transform: uppercase;
                        font-size: 16px;
                    }
                    header ul {
                        padding: 0;
                        list-style: none;
                    }
                    header li {
                        float: left;
                        display: inline;
                        padding: 0 20px 0 20px;
                    }
                    header #branding {
                        float: left;
                    }
                    header #branding h1 {
                        margin: 0;
                        font-size: 24px;
                        font-weight: bold;
                    }
                    header nav {
                        float: right;
                        margin-top: 10px;
                    }
                    .content {
                        padding: 20px;
                        background: #fff;
                        margin-top: 20px;
                    }
                    .grid-container {
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        grid-gap: 20px;
                    }
                    .chart {
                        background: #fff;
                        padding: 20px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                </style>
            </head>
            <body>
                <header>
                    <div class="container">
                        <div id="branding">
                            <h1>JUnit Test Results Dashboard</h1>
                        </div>
                    </div>
                </header>
                <div class="container">
                    <div class="content">
                        <div class="grid-container">
            """
        )

        dashboard.write('<div class="chart">')
        dashboard.write(
            pio.to_html(
                fig_status_pie,
                full_html=False,
                include_plotlyjs="cdn",
                config={"displaylogo": False},
            )
        )
        dashboard.write("</div>")

        dashboard.write('<div class="chart">')
        dashboard.write(
            pio.to_html(
                fig_top_failures,
                full_html=False,
                include_plotlyjs="cdn",
                config={"displaylogo": False},
            )
        )
        dashboard.write("</div>")

        dashboard.write('<div class="chart">')
        dashboard.write(
            pio.to_html(
                fig_failed_suites,
                full_html=False,
                include_plotlyjs="cdn",
                config={"displaylogo": False},
            )
        )
        dashboard.write("</div>")

        dashboard.write('<div class="chart">')
        dashboard.write(
            pio.to_html(
                fig_slow_tests,
                full_html=False,
                include_plotlyjs="cdn",
                config={"displaylogo": False},
            )
        )
        dashboard.write("</div>")

        dashboard.write(
            """
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
        )


if __name__ == "__main__":
    main()
