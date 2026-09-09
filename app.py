from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="sk">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6595281967559794"
     crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kalkulačka mzdy Rakúsko</title>
<style>
body {

    font-family: Arial, sans-serif;
    background: #eef3f8;
    margin: 0;
    padding: 20px;
}
.box {
    max-width: 500px;
    margin: auto;
    background: #ffffff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.15);
}
h1 {
    text-align: center;
}
label {
    display: block;
    margin-top: 12px;
    font-weight: bold;
}
input {
    width: 100%;
    box-sizing: border-box;
    padding: 12px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 16px;
}
button {
    width: 100%;
    padding: 14px;
    margin-top: 20px;
    border: 0;
    border-radius: 8px;
    background: #222;
    color: white;
    font-size: 17px;
}
.result {
    margin-top: 25px;
    padding: 20px;
    background: #f8fafc;
    border-radius: 15px;
    border: 1px solid #e2e8f0;
}

.result p {
    padding: 8px 0;
    margin: 0;
    border-bottom: 1px solid #e5e7eb;
}

.result h2 {
    text-align: center;
    margin-top: 25px;
    padding: 15px;
    border-radius: 12px;
    background: #dcfce7;
    color: #166534;
    font-size: 28px;
}

.result h3 {
    margin-top: 25px;
    text-align: center;
}
.warning {
    margin-top: 15px;
    font-size: 13px;
    color: #555;
}
</style>
</head>

<body>
<div class="box">

<h1>🇦🇹 Kalkulačka mzdy</h1>

<form method="POST">

<label>Bežné hodiny</label>
<input type="number" step="0.01" name="hodiny" value="160" required>

<label>Mzda €/hodina</label>
<input type="number" step="0.01" name="mzda" value="12.68" required>

<label>Nadčasy</label>
<input type="number" step="0.01" name="nadcasy" value="10" required>

<label>Nadčasový príplatok %</label>
<input type="number" step="0.01" name="nadcas_percent" value="50" required>

<label>Nočné hodiny</label>
<input type="number" step="0.01" name="nocne" value="10" required>

<label>Nočný príplatok %</label>
<input type="number" step="0.01" name="noc_percent" value="25" required>

<label>Počet detí</label>
<input type="number" min="0" max="20" name="deti" value="3" required>
<label>Bundesland</label>
<select name="bundesland">
    <option value="Wien">Wien</option>
    <option value="Niederoesterreich">Niederösterreich</option>
    <option value="Burgenland">Burgenland</option>
    <option value="Steiermark">Steiermark</option>
    <option value="Kaernten">Kärnten</option>
    <option value="Oberoesterreich">Oberösterreich</option>
    <option value="Salzburg">Salzburg</option>
    <option value="Tirol">Tirol</option>
    <option value="Vorarlberg">Vorarlberg</option>
</select>
    <label>13. a 14. plat</label>
    <select name="sonderzahlungen">
        <option value="ano">Áno</option>
        <option value="nie">Nie</option>
    </select>

    <button type="submit" style="width:100%;padding:15px;font-size:18px;border:0;border-radius:10px;background:#2563eb;color:white;font-weight:bold;cursor:pointer;">🧮 Vypočítať mzdu</button>
</form>

{% if result %}
<div class="result">
<h2>Výsledok</h2>

<p>Základná mzda: <b>{{ result.zaklad }} €</b></p>
<p>Nadčasy: <b>{{ result.mzda_nadcas }} €</b></p>
<p>Nadčasový príplatok: <b>{{ result.nadcas_priplatok }} €</b></p>
<p>Nočný príplatok: <b>{{ result.nocny_priplatok }} €</b></p>

<hr>

<p>BRUTTO mesačne: <b>{{ result.brutto }} €</b></p>
<p>Sociálne odvody: <b>{{ result.socialne }} €</b></p>
<p>Daň pred bonusom: <b>{{ result.dan }} €</b></p>
<p>Familienbonus: <b>{{ result.familienbonus }} €</b></p>
<p>Daň po bonuse: <b>{{ result.dan_po_bonuse }} €</b></p>

    <p>13. plat brutto: <b>{{ result.sonderzahlung_brutto }} €</b></p>
    <p>13. a 14. plat spolu netto: <b>{{ result.netto_13_14 }} €</b></p>
    <p>13. plat netto: <b>{{ result.netto_13_plat }} €</b></p>
    <p>14. plat netto: <b>{{ result.netto_14_plat }} €</b></p>
    <hr>
    <h3>Ročný prehľad</h3>
    <p>Ročné BRUTTO: <b>{{ result.rocne_brutto }} €</b></p>
    <p>Ročné NETTO: <b>{{ result.rocne_netto }} €</b></p>
<h2>NETTO: {{ result.netto }} €</h2>
</div>
{% endif %}

<div class="warning">
⚠️ Ide o orientačný výpočet. Skutočná mzda závisí od pracovnej zmluvy,
odvodov, daní a individuálnych podmienok.
</div>

</div>
</body>
</html>
"""

def vypocitaj_dan(zaklad):
    if zaklad <= 13539:
        dan = 0
    elif zaklad <= 21992:
        dan = (zaklad - 13539) * 0.20
    elif zaklad <= 36458:
        dan = (21992 - 13539) * 0.20
        dan += (zaklad - 21992) * 0.30
    elif zaklad <= 70365:
        dan = (21992 - 13539) * 0.20
        dan += (36458 - 21992) * 0.30
        dan += (zaklad - 36458) * 0.40
    elif zaklad <= 104859:
        dan = (21992 - 13539) * 0.20
        dan += (36458 - 21992) * 0.30
        dan += (70365 - 36458) * 0.40
        dan += (zaklad - 70365) * 0.48
    elif zaklad <= 1000000:
        dan = (21992 - 13539) * 0.20
        dan += (36458 - 21992) * 0.30
        dan += (70365 - 36458) * 0.40
        dan += (104859 - 70365) * 0.48
        dan += (zaklad - 104859) * 0.50
    else:
        dan = (21992 - 13539) * 0.20
        dan += (36458 - 21992) * 0.30
        dan += (70365 - 36458) * 0.40
        dan += (104859 - 70365) * 0.48
        dan += (1000000 - 104859) * 0.50
        dan += (zaklad - 1000000) * 0.55

    return max(0, dan - 496)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        hodiny = float(request.form["hodiny"])
        mzda = float(request.form["mzda"])
        nadcasy = float(request.form["nadcasy"])
        nadcas_percent = float(request.form["nadcas_percent"])
        nocne = float(request.form["nocne"])
        noc_percent = float(request.form["noc_percent"])
        sonderzahlungen = request.form["sonderzahlungen"]
        deti = int(request.form["deti"])
        bundesland = request.form["bundesland"]
        mzda_nadcas = nadcasy * mzda
        zaklad = hodiny * mzda
        nadcas_priplatok = mzda_nadcas * nadcas_percent / 100
        nocny_priplatok = nocne * mzda * noc_percent / 100

        brutto = (
            zaklad
            + mzda_nadcas
            + nadcas_priplatok
            + nocny_priplatok
        )

        sonderzahlung_brutto = brutto if sonderzahlungen == "ano" else 0
        av_sonder = 0.00 if sonderzahlung_brutto <= 2225 else (0.01 if sonderzahlung_brutto <= 2427 else (0.02 if sonderzahlung_brutto <= 2630 else 0.0295))
        sonderzahlung_sv = sonderzahlung_brutto * (0.0387 + 0.1025 + av_sonder)
        sonderzahlung_zaklad = max(0, sonderzahlung_brutto - sonderzahlung_sv)
        sonderzahlung_dan_spolu = max(0, (sonderzahlung_zaklad * 2 - 620) * 0.06) if sonderzahlungen == "ano" else 0
        sonderzahlung_netto = max(0, sonderzahlung_zaklad - sonderzahlung_dan_spolu / 2) if sonderzahlungen == "ano" else 0
        netto_13_14 = sonderzahlung_netto * 2 if sonderzahlungen == "ano" else 0
        netto_13_plat = sonderzahlung_netto if sonderzahlungen == "ano" else 0
        netto_14_plat = sonderzahlung_netto if sonderzahlungen == "ano" else 0
        if brutto <= 2225:
            av = 0.00
        elif brutto <= 2427:
            av = 0.01
        elif brutto <= 2630:
            av = 0.02
        else:
            av = 0.0295

        if bundesland == "Wien":
            wf = 0.0075
        else:
            wf = 0.0050

        if bundesland == "Wien":
            wf = 0.0075
        else:
            wf = 0.0050

        socialne = brutto * (0.0387 + 0.1025 + 0.005 + wf + av)
        rocny_zaklad = (brutto - socialne) * 12

        dan_rocne = vypocitaj_dan(rocny_zaklad)
        familienbonus_rocne = deti * 166.68 * 12

        dan_po_bonuse_rocne = max(
            0,
            dan_rocne - familienbonus_rocne
        )

        dan = dan_rocne / 12
        familienbonus = familienbonus_rocne / 12
        dan_po_bonuse = dan_po_bonuse_rocne / 12

        netto = brutto - socialne - dan_po_bonuse
        rocne_brutto = brutto * 12 + sonderzahlung_brutto * 2
        rocne_netto = netto * 12 + netto_13_14

        result = {
            "zaklad": f"{zaklad:.2f}",
            "mzda_nadcas": f"{mzda_nadcas:.2f}",
            "nadcas_priplatok": f"{nadcas_priplatok:.2f}",
            "nocny_priplatok": f"{nocny_priplatok:.2f}",
            "brutto": f"{brutto:.2f}",
            "socialne": f"{socialne:.2f}",
            "dan": f"{dan:.2f}",
            "familienbonus": f"{familienbonus:.2f}",
            "dan_po_bonuse": f"{dan_po_bonuse:.2f}",
            "sonderzahlung_brutto": f"{sonderzahlung_brutto:.2f}",
            "sonderzahlung_netto": f"{sonderzahlung_netto:.2f}",
            "netto_13_14": f"{netto_13_14:.2f}",
            "netto_13_plat": f"{netto_13_plat:.2f}",
            "netto_14_plat": f"{netto_14_plat:.2f}",
            "rocne_brutto": f"{rocne_brutto:.2f}",
            "rocne_netto": f"{rocne_netto:.2f}",
            "netto": f"{netto:.2f}"
        }

    return render_template_string(HTML, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

