
import xml.etree.ElementTree as ET

def clean_text(text):
    return text.replace("\n", "").replace("\r", "").strip()

def parse_law_xml(xml_path, query):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    조문들 = []
    found = False

    법령명 = root.findtext("기본정보/법령명_한글")
    원문링크 = "https://www.law.go.kr/법령/" + 법령명.replace(" ", "")

    for 조문 in root.findall("조문/조문단위"):
        조번호 = 조문.findtext("조문번호")
        조제목 = clean_text(조문.findtext("조문제목") or "")
        본문 = clean_text(조문.findtext("조문내용") or "")
        if 본문.startswith(f"제{조번호}조"):
            본문 = 본문[len(f"제{조번호}조"):]
        항_list = 조문.findall("항")
        조문_text = f"제{조번호}조({조제목})"
        if not 항_list:
            if query in 본문:
                조문_text += " " + 본문
                조문들.append(조문_text)
                found = True
            continue

        first = True
        for 항 in 항_list:
            항번호 = 항.findtext("항번호", "").strip()
            항내용 = clean_text(항.findtext("항내용") or "")
            항text = 항내용
            if query in 항내용:
                if first:
                    조문_text += " " + 항text
                    first = False
                else:
                    조문_text += f"\n  {항text}"
                found = True

            for 호 in 항.findall("호"):
                호번호 = clean_text(호.findtext("호번호") or "")
                호내용 = clean_text(호.findtext("호내용") or "")
                if query in 호내용:
                    if first:
                        조문_text += " " + 항text
                        first = False
                    조문_text += f"\n  {호번호} {호내용}"
                    found = True

                for 목 in 호.findall("목"):
                    목내용 = clean_text(목.findtext("목내용") or "")
                    if query in 목내용:
                        if first:
                            조문_text += " " + 항text
                            first = False
                        조문_text += f"\n    - {목내용}"
                        found = True

        if found:
            조문들.append(조문_text)

    return {"법령명": 법령명, "조문들": 조문들, "원문링크": 원문링크} if 조문들 else None
