import json
import re
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.ebay.com/b/Wristwatches/31387/bn_2408451?_udlo=500&LH_Sold=1&Brand=A%252E%2520Lange%2520%2526%2520S%25C3%25B6hne%7CAlain%2520Silberstein%7CAngelus%7CAntoine%2520Preziuso%7CAquaswiss%7CArnold%2520%2526%2520Son%7CAudemars%2520Piguet%7CAzimuth%7CBaume%2520%2526%2520Mercier%7CBedat%2520%2526%2520Co%7CBlancpain%7CBOVET%7CBoucheron%7CBOMBERG%7CBreguet%7CBremont%7CBreitling%7CBucherer%7CBvlgari%7CCarl%2520F%252E%2520Bucherer%7CCarrera%7CCartier%7CChaumet%7CChopard%7CChristopher%2520Ward%7CChronographe%2520Suisse%7CChronoswiss%7CCuervo%2520y%2520Sobrinos%7CCvstos%7Cde%2520GRISOGONO%7CDeWitt%7CDOXA%7CDubey%2520%2526%2520Schaldenbrand%7CEBEL%7CEberhard%2520%2526%2520Co%252E%7CEberhard%7CErnest%2520Borel%7CF%252EP%252E%2520Journe%7CFavre%2520Leuba%7CFranck%2520Muller%7CGerminal%2520Voltaire%7CGirard%252DPerregaux%7CGlash%25C3%25BCtte%2520Original%7CGrand%2520Seiko%7CG%25C3%25BCbelin%7CH%252E%2520Moser%7CH%2526M%7CHarry%2520Winston%7CHublot%7CIWC%7CJACOB%2520%2526%2520Co%252E%7CJaquet%2520Droz%7CJEANRICHARD%7CJorg%2520Gray%7CJuvenia%7CLemania%7CLe%2520Jour%7CLeonidas%7CLongines%7CLouis%2520Vuitton%7CMAD%7CMaurice%2520Lacroix%7CMathey%252DTissot%7CMeisterSinger%7CMichel%2520Jordi%7CMontblanc%7CMOMODESIGN%7CNivada%2520Grenchen%7CNIVADA%7COris%7CPanerai%7CParmigiani%2520Fleurier%7CPatek%2520Philippe%7CPaul%2520Breguette%7CPaul%2520Picot%7CPerrelet%7CPiaget%7CRalph%2520Lauren%7CRichard%2520Mille%7CRoger%2520Dubuis%7CRolex%7CTAG%2520Heuer%7CSzanto%7CTavannes%7CTiffany%2520%2526%2520Co%252E%7CU%252DBoat%7CUlysse%2520Nardin%7CTourneau%7CUniversal%2520Gen%25C3%25A8ve%7CVacheron%2520Constantin%7CVan%2520Cleef%2520%2526%2520Arpels%7CVulcain%7CWaltham%7CYema%7CWakmann&mag=1"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8"
}

products_data = []
page = 1

while True:
    url = f"{BASE_URL}&_pgn={page}"
    print(f"📄 Scrapeando página {page}")

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")

    products = soup.select("div.brwrvr__item-card__body")

    if page > 10:
        print("🚫 No hay más productos.")
        break

    for product in products:
        title_el = product.select_one("h3.bsig__title__text")
        price_el = product.select_one("span.bsig__price--displayprice")
        img_el = product.select_one("img")
        link_el = product.select_one("a[href]")

        title = title_el.get_text(strip=True) if title_el else "Sin título"

        price = None

        if price_el:
         price_raw = price_el.get_text()
         price = float(re.sub(r"[^\d.]", "", price_raw))

        image = (
            img_el.get("data-src")
            or img_el.get("data-img-src")
            or img_el.get("src")
            if img_el else "Sin imagen"
        )

        link = link_el["href"] if link_el else "Sin link"

        products_data.append({
            "title": title,
            "price": price,
            "image": image,
            "link": link
        })

    page += 1
    time.sleep(1.5)

with open("extractor_ebay_sold.json", "w", encoding="utf-8") as f:
    json.dump(products_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Total productos guardados: {len(products_data)}")
