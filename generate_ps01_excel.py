#!/usr/bin/env python3
"""
generate_ps01_excel.py - Generates the official PS-01 submission Excel file for CodeGlia.
Usage:
    python generate_ps01_excel.py
"""
import sys
import json
import os
import glob
import openpyxl

def load_scan_report(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "findings" in data:
        return data["findings"]
    elif isinstance(data, list):
        return data
    else:
        print("⚠️ Unrecognized report schema; returning empty list.")
        return []

def load_f1_score(eval_path):
    try:
        with open(eval_path, "r", encoding="utf-8") as f:
            for line in f:
                if "F1" in line:
                    return float(line.strip().split(":")[-1])
    except Exception:
        pass
    return None

def find_latest_file(pattern):
    files = glob.glob(pattern)
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def generate_excel(report_path, eval_path, output_excel):
    findings = load_scan_report(report_path)
    f1 = load_f1_score(eval_path)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stage 1 Submission"

    headers = [
        "Ser",
        "Name of Application Tested",
        "Language",
        "Vulnerability Found",
        "CVE",
        "File Name",
        "Line of Code",
        "Detection Accuracy (F1)"
    ]
    ws.append(headers)

    for idx, item in enumerate(findings, start=1):
        file_name = os.path.basename(item.get("file", ""))
        language = file_name.split(".")[-1].upper()
        vuln = item.get("cwe", "N/A")
        cve = item.get("cve", "N/A")
        line = item.get("line", "")
        ws.append([
            idx,
            "PS01_Test_Set",       # Name of application under test
            language,
            vuln,
            cve,
            file_name,
            line,
            f"{f1:.3f}" if f1 is not None else ""
        ])

    for col in ws.columns:
        max_len = max(len(str(cell.value)) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 2

    wb.save(output_excel)
    print(f"✅ Excel generated: {output_excel}")
    print(f"📊 F1 Score used: {f1:.3f}" if f1 else "⚠️ F1 not found in evaluation file")

def main():
    report_path = find_latest_file("output/scan_report.json")
    eval_path = find_latest_file("evaluation/evaluation_summary.txt")

    if not report_path:
        print("⚠️ No scan_report.json file found in output/ directory.")
        sys.exit(1)
    if not eval_path:
        print("⚠️ No evaluation_summary.txt file found in evaluation/ directory.")
        sys.exit(1)

    output_excel = "GC_PS_01_CodeGlia.xlsx"
    print(f"Using scan report: {report_path}")
    print(f"Using evaluation summary: {eval_path}")
    generate_excel(report_path, eval_path, output_excel)

if __name__ == "__main__":
    main()