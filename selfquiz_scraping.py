import re, sys, json, csv, pathlib
from bs4 import BeautifulSoup

def norm(s: str) -> str:
    if s is None: return ""
    s = s.replace("\u00A0", " ")
    s = re.sub(r"\s+", " ", s.strip())
    return s

def parse_quiz(html: str, source_file: str):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for q in soup.select("div.que.multichoice"):
        qtext_el = q.select_one(".qtext")
        if not qtext_el:
            continue
        qtext = norm(qtext_el.get_text(" ", strip=True))

        options = []
        for row in q.select(".answer > div"):
            label_el = row.select_one(".answernumber")
            content_el = row.select_one('[data-region="answer-label"] .flex-fill')
            if not label_el or not content_el:
                continue
            letter = norm(label_el.get_text()).rstrip(".")
            content = norm(content_el.get_text(" ", strip=True))
            is_correct = (
                ("correct" in (row.get("class") or [])) or
                (row.select_one(".fa-check.text-success") is not None) or
                (row.select_one('input[type="radio"][checked]') is not None)
            )
            options.append({"letter": letter, "text": content, "is_correct": is_correct})

        # フィードバック照合（保険）
        if options and not any(o["is_correct"] for o in options):
            right_el = q.select_one(".outcome .rightanswer")
            if right_el:
                m = re.search(r":\s*(.*)$", right_el.get_text(strip=True))
                if m:
                    right_text = norm(m.group(1))
                    for o in options:
                        if norm(o["text"]) == right_text:
                            o["is_correct"] = True
                            break

        answer_letters = [o["letter"] for o in options if o["is_correct"]]
        # source_fileを最初に
        results.append({
            "source_file": source_file,
            "question": qtext,
            "options": [{"letter": o["letter"], "text": o["text"]} for o in options],
            "answer": answer_letters[0] if answer_letters else None
        })
    return results

def to_csv(rows, csv_path):
    # 1行に：source_file / question / a / b / c / d / answer の順で出力
    headers = ["source_file", "question", "a", "b", "c", "d", "answer"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            row = {
                "source_file": r.get("source_file", ""),
                "question": r["question"],
                "answer": r["answer"]
            }
            for opt in r["options"]:
                row[opt["letter"]] = opt["text"]
            w.writerow(row)

if __name__ == "__main__":
    html_dir = pathlib.Path("html")
    if not html_dir.exists() or not html_dir.is_dir():
        print("html directory not found. Please create a 'html' folder and put your HTML files in it.")
        sys.exit(1)

    filepaths = sorted(str(p) for p in html_dir.glob("*.html"))
    if not filepaths:
        print("No HTML files found in 'html' directory.")
        sys.exit(1)

    all_data = []
    for idx, filepath in enumerate(filepaths, 1):
        print(f"Processing [{idx}]: {filepath}")
        html_path = pathlib.Path(filepath)
        if not html_path.exists():
            print(f"File not found: {filepath}")
            continue
        html = html_path.read_text(encoding="utf-8")

        data = parse_quiz(html, str(html_path))
        all_data.extend(data)

    out_json = pathlib.Path("quiz.json")
    out_json.write_text(json.dumps(all_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON -> {out_json}")

    out_csv = pathlib.Path("quiz.csv")
    to_csv(all_data, out_csv)
    print(f"CSV  -> {out_csv}")
