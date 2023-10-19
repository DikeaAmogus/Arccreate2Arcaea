def getRatingClass(chart, getChartDesigner, getJacketDesigners):
    alias = chart.get("alias", chart.get("charter", ""))
    if "\r" in alias:
        alias = alias.split("\r")[0]
    if "\n" in alias:
        alias = alias.split("\n")[0]
    if "\r" in alias:
        alias = alias.split("\r")[0]
    if "\u000b" in alias:
        alias = alias.split("\u000b")[0]
    if "<size=75%>" in alias:
        alias = alias.split("<size=75%>")[0]
    if "</size>" in alias:
        alias = alias.strip("")
    if alias.startswith("<size=75%></size>"):
        alias = alias.replace("<size=75%></size>", "")
    if alias.endswith("<size=75%>"):
        alias = alias.replace("<size=75%>", "")
    alias = alias.strip()
    chartDesigner = getChartDesigner[chart["chartPath"]] = alias
    jacketDesigner = getJacketDesigners[chart["chartPath"]] = chart.get(
        "illustrator", ""
    ).replace("\u000b", "")
    if jacketDesigner == "-":
        jacketDesigner = ""
    cc = chart.get("chartConstant", 0)
    rating = int(cc)
    rating_decimal = cc % 1
    ratingPlus = rating_decimal >= 0.7
    if int(cc) <= 9 and float(cc) <= 9.6:
        ratingPlus = False
    getRatingClasses = {
        "ratingClass": int(chart["chartPath"][0]),
        "chartDesigner": chartDesigner,
        "jacketDesigner": jacketDesigner,
        "rating": rating,
    }
    if ratingPlus:
        getRatingClasses["ratingPlus"] = True
    audioPath = chart.get("audioPath", "")
    jacketPath = chart.get("jacketPath", "")
    audioOverride = f"{chart['chartPath'][0]}.ogg"
    jacketOverride = f"{chart['chartPath'][0]}.jpg"
    if audioOverride in audioPath:
        getRatingClasses["audioOverride"] = True
    if jacketOverride in jacketPath:
        getRatingClasses["jacketOverride"] = True
    return getRatingClasses
