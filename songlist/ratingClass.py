def getRatingClass(chart, getChartDesigner, getJacketDesigners):
    alias = chart.get("alias", chart.get("charter", ""))
    if "\r" in alias:  # this is so fucking dumb i swear.
        alias = alias.split("\r")[0]  # this is so fucking dumb i swear.
    if "\n" in alias:  # this is so fucking dumb i swear.
        alias = alias.split("\n")[0]  # this is so fucking dumb i swear.
    if "\r" in alias:  # this is so fucking dumb i swear.
        alias = alias.split("\r")[0]  # this is so fucking dumb i swear.
    if "\u000b" in alias:  # this is so fucking dumb i swear.
        alias = alias.split("\u000b")[0]  # this is so fucking dumb i swear.
    if "</size>" in alias:  # this is so fucking dumb i swear.
        alias = alias.strip("")  # this is so fucking dumb i swear.
    if "<size=75%>" in alias:  # this is so fucking dumb i swear.
        alias = alias.strip("")  # this is so fucking dumb i swear.
    if alias.startswith("<size=75%></size>"):  # this is so fucking dumb i swear.
        alias = alias.replace(
            "<size=75%></size>", ""
        )  # this is so fucking dumb i swear.
    if alias.endswith("<size=75%>"):  # this is so fucking dumb i swear.
        alias = alias.replace("<size=75%>", "")  # this is so fucking dumb i swear.
    alias = alias.strip()  # this is so fucking dumb i swear.
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
    if not jacketOverride == f"{chart['chartPath'][0]}.jpg":
        jacketOverride = f"{chart['chartPath'][0]}.png"
    if audioOverride in audioPath:
        getRatingClasses["audioOverride"] = True
    if jacketOverride in jacketPath:
        getRatingClasses["jacketOverride"] = True
    return getRatingClasses
