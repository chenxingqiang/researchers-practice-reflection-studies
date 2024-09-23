import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def mermaid_to_image(mermaid_code, output_file, format="svg"):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mermaid Diagram</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    </head>
    <body>
        <div class="mermaid">
        {mermaid_code}
        </div>
        <script>
            mermaid.initialize({{ startOnLoad: true }});
            function getSVG() {{
                var svg = document.querySelector('.mermaid svg');
                return svg.outerHTML;
            }}
        </script>
    </body>
    </html>
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        with open("temp.html", "w", encoding="utf-8") as f:
            f.write(html)

        driver.get("file://" + os.path.abspath("temp.html"))

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mermaid"))
        )

        # Wait for Mermaid to finish rendering
        driver.execute_script(
            "return new Promise(resolve => setTimeout(resolve, 1000))"
        )

        # Get the SVG content
        svg_content = driver.execute_script("return getSVG()")

        if format.lower() == "svg":
            # Save as SVG
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(svg_content)
        elif format.lower() == "png":
            # Convert SVG to PNG using cairosvg
            import cairosvg

            png_data = cairosvg.svg2png(bytestring=svg_content.encode("utf-8"))
            with open(output_file, "wb") as f:
                f.write(png_data)
        else:
            raise ValueError("Unsupported format. Use 'svg' or 'png'.")

        print(f"Mermaid diagram saved as {format.upper()}: {output_file}")
        return True

    except Exception as e:
        print(f"Error generating image for Mermaid diagram: {e}")
        return False
    finally:
        driver.quit()
        if os.path.exists("temp.html"):
            os.remove("temp.html")
