import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_all_grand_prix(season_id='season-2025-2071'):
    base = "https://www.fia.com"
    url = f"{base}/documents/championships/fia-formula-one-world-championship-14/season/{season_id}/"

    driver_path = r"D:\SoftwareEngineer\codes\f1_downloader_project\edgedriver_win64\msedgedriver.exe"

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")  # 可选，调试时建议注释掉

    service = EdgeService(executable_path=driver_path)
    driver = webdriver.Edge(service=service, options=options)

    try:
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "facetapi_select_facet_form_2"))
        )

        grand_prix_map = {}
        select = driver.find_element(By.ID, "facetapi_select_facet_form_2")
        options = select.find_elements(By.TAG_NAME, "option")
        for opt in options:
            name = opt.text.strip()
            val = opt.get_attribute("value")
            if name and val and "event" in val:
                grand_prix_map[name] = f"{base}{val}"
        return grand_prix_map
    finally:
        driver.quit()


if __name__ == "__main__":
    season = "season-2025-2071"
    grand_prix_data = get_all_grand_prix(season)
    with open("grand_prix_list.json", "w", encoding="utf-8") as f:
        json.dump(grand_prix_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(grand_prix_data)} Grand Prix entries to grand_prix_list.json")
