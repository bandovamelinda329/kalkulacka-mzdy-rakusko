from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="sk">
<head>
<meta name="google-adsense-account" content="ca-pub-6595281967559794"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6595281967559794"
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

<h1>🌍 Kalkulačka mzdy</h1>
<div style="text-align:center;margin:15px 0;">
    <button type="button" onclick="setLanguage('sk')">🇸🇰 SK</button>
    <button type="button" onclick="setLanguage('de')">🇩🇪 DE</button>
    <button type="button" onclick="setLanguage('en')">🇬🇧 EN</button>
</div><p style="text-align:center;color:#64748b;font-size:15px;">
  Mzdová kalkulačka pre Rakúsko 🇦🇹
</p>
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
<h2 id="result-title">Výsledok</h2>
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
<h3 id="year-title">Ročný prehľad</h3>    <p>Ročné BRUTTO: <b>{{ result.rocne_brutto }} €</b></p>
<h2 id="netto-title">NETTO: {{ result.netto }} €</h2><h2>NETTO: {{ result.netto }} €</h2>
</div>
{% endif %}


<section style="margin-top:35px;text-align:left;line-height:1.7;">
<h2>🇦🇹 Ako funguje výpočet mzdy v Rakúsku?</h2>

<p>
Táto kalkulačka mzdy je určená pre ľudí pracujúcich v Rakúsku.
Pomáha orientačne vypočítať mesačnú mzdu podľa počtu pracovných hodín,
hodinovej mzdy, nadčasov, nočných hodín, detí a vybraného spolkového
štátu.
</p>

<h3>💶 Brutto a netto mzda</h3>
<p>
Brutto mzda je suma pred odpočítaním sociálnych odvodov a dane.
Netto mzda je suma, ktorá po zohľadnení príslušných odvodov a dane
zostáva zamestnancovi. Skutočná výplata sa môže líšiť podľa pracovnej
zmluvy, kolektívnej zmluvy a osobnej situácie zamestnanca.
</p>

<h3>⏱️ Nadčasy</h3>
<p>
Pri práci nad rámec bežného pracovného času môže vzniknúť nárok na
nadčasovú odmenu alebo príplatok. Výška príplatku závisí od pracovnej
zmluvy a príslušnej kolektívnej alebo zákonnej úpravy.
</p>

<h3>🌙 Nočná práca</h3>
<p>
Za nočnú prácu môže podľa pracovných podmienok patriť osobitný príplatok.
Jeho výška sa môže líšiť podľa odvetvia, pracovnej zmluvy a kolektívnej
zmluvy.
</p>

<h3>👨‍👩‍👧 Deti a Familienbonus</h3>
<p>
Pri zamestnancoch s deťmi môžu mať rodinné daňové zvýhodnenia vplyv na
výslednú daňovú záťaž. Kalkulačka preto umožňuje zadať počet detí.
Konkrétny nárok však závisí od individuálnej situácie.
</p>

<h3>🏠 Spolková krajina</h3>
<p>
Kalkulačka umožňuje vybrať spolkovú krajinu, napríklad Wien,
Niederösterreich, Burgenland alebo Steiermark. Niektoré pracovné
podmienky a výpočty môžu závisieť od odvetvia a pracovných pravidiel.
</p>

<h3>❓ Na čo kalkulačka slúži?</h3>
<p>
Výsledok je orientačný a môže slúžiť ako pomôcka pri porovnávaní
pracovných ponúk alebo pri plánovaní mesačného príjmu. Nenahrádza
oficiálnu výplatnú pásku ani individuálny výpočet zamestnávateľa.
</p>

<h3>📌 Dôležité upozornenie</h3>
<p>
Výpočet je informatívny. Skutočná mzda môže byť odlišná podľa pracovnej
zmluvy, kolektívnej zmluvy, sociálnych odvodov, dane, daňových
zvýhodnení, príplatkov a ďalších individuálnych podmienok.
</p>
</section>

<div class="warning">
⚠️ Ide o orientačný výpočet. Skutočná mzda závisí od pracovnej zmluvy,
odvodov, daní a individuálnych podmienok.
</div>

</div>
</body>
</html>
<script>
function setLanguage(lang) {

    const translations = {
        sk: {
            title: "🌍 Kalkulačka mzdy",
            subtitle: "Mzdová kalkulačka pre Rakúsko 🇦🇹",
            hours: "Bežné hodiny",
            wage: "Mzda €/hodina",
            overtime: "Nadčasy",
            overtimePercent: "Nadčasový príplatok %",
            night: "Nočné hodiny",
            nightPercent: "Nočný príplatok %",
            children: "Počet detí",
            state: "Bundesland",
            bonus: "13. a 14. plat",
            calculate: "🧮 Vypočítať mzdu"
resultTitle: "Výsledok",
base: "Základná mzda:",
overtimeResult: "Nadčasy:",
overtimeBonusResult: "Nadčasový príplatok:",
nightBonusResult: "Nočný príplatok:",
grossMonthly: "BRUTTO mesačne:",
social: "Sociálne odvody:",
taxBefore: "Daň pred bonusom:",
familyBonusResult: "Familienbonus:",
taxAfter: "Daň po bonuse:",
salary13Gross: "13. plat brutto:",
salary13_14Net: "13. a 14. plat spolu netto:",
salary13Net: "13. plat netto:",
salary14Net: "14. plat netto:",
annualOverview: "Ročný prehľad",
annualGross: "Ročné BRUTTO:",
annualNet: "Ročné NETTO:",
netResult: "NETTO:"
        },
        de: {
            title: "🌍 Gehaltsrechner",
            subtitle: "Gehaltsrechner für Österreich 🇦🇹",
            hours: "Normale Arbeitsstunden",
            wage: "Lohn €/Stunde",
            overtime: "Überstunden",
            overtimePercent: "Überstundenzuschlag %",
            night: "Nachtstunden",
            nightPercent: "Nachtzuschlag %",
            children: "Anzahl der Kinder",
            state: "Bundesland",
            bonus: "13. und 14. Gehalt",
            calculate: "🧮 Gehalt berechnen"
resultTitle: "Ergebnis",
base: "Grundgehalt:",
overtimeResult: "Überstunden:",
overtimeBonusResult: "Überstundenzuschlag:",
nightBonusResult: "Nachtzuschlag:",
grossMonthly: "Monatliches BRUTTO:",
social: "Sozialversicherungsbeiträge:",
taxBefore: "Steuer vor Bonus:",
familyBonusResult: "Familienbonus:",
taxAfter: "Steuer nach Bonus:",
salary13Gross: "13. Gehalt brutto:",
salary13_14Net: "13. und 14. Gehalt netto zusammen:",
salary13Net: "13. Gehalt netto:",
salary14Net: "14. Gehalt netto:",
annualOverview: "Jahresübersicht",
annualGross: "Jahres-BRUTTO:",
annualNet: "Jahres-NETTO:",
netResult: "NETTO:"        },
        en: {
            title: "🌍 Salary Calculator",
            subtitle: "Salary calculator for Austria 🇦🇹",
            hours: "Regular hours",
            wage: "Wage €/hour",
            overtime: "Overtime",
            overtimePercent: "Overtime bonus %",
            night: "Night hours",
            nightPercent: "Night bonus %",
            children: "Number of children",
            state: "Federal state",
            bonus: "13th and 14th salary",
            calculate: "🧮 Calculate salary",
resultTitle: "Result",
base: "Base salary:",
overtimeResult: "Overtime:",
overtimeBonusResult: "Overtime bonus:",
nightBonusResult: "Night bonus:",
grossMonthly: "Monthly GROSS:",
social: "Social contributions:",
taxBefore: "Tax before bonus:",
familyBonusResult: "Family bonus:",
taxAfter: "Tax after bonus:",
salary13Gross: "13th salary gross:",
salary13_14Net: "13th and 14th salary net total:",
salary13Net: "13th salary net:",
salary14Net: "14th salary net:",
annualOverview: "Annual overview",
annualGross: "Annual GROSS:",
annualNet: "Annual NET:",
netResult: "NET:"
        }
    };

    const t = translations[lang];

    document.querySelector("h1").textContent = t.title;
    document.querySelector("h1").nextElementSibling.nextElementSibling.textContent = t.subtitle;

    const labels = document.querySelectorAll("label");

    labels[0].textContent = t.hours;
    labels[1].textContent = t.wage;
    labels[2].textContent = t.overtime;
    labels[3].textContent = t.overtimePercent;
    labels[4].textContent = t.night;
    labels[5].textContent = t.nightPercent;
    labels[6].textContent = t.children;
    labels[7].textContent = t.state;
    labels[8].textContent = t.bonus;

    document.querySelector("form button").textContent = t.calculate;
document.getElementById("result-title").textContent = t.resultTitle;
document.getElementById("year-title").textContent = t.annualOverview;
document.getElementById("netto-title").textContent = t.netResult;
}
</script>"""

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

