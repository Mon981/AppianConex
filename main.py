import sys
from conexAPI import get_product_map
from scrapping import scrape_prices
from appian_post import post_results_to_appian
from progress import ConnectingAnimator, ProgressBarAnimator

def main():
    args = sys.argv[1:]

    if args and args[0].lower() == "upgrade":
        products = get_product_map()[:3]  

        connecting = ConnectingAnimator(max_dots=5, interval=0.5)
        progress = ProgressBarAnimator(max_hashes=30, interval=0.5)

        connecting.start()

        
        def on_scraping_ready():
            connecting.stop()
            # print() 
            progress.start()

        scraped = scrape_prices(products, on_ready=on_scraping_ready)

        progress.stop("Proceso completado")        
        payload = [
            {
                "id": i + 1,
                "producto": p["nombre"],          
                "precio": p["precio_original"],   
                "precio_nuevo": p["precio_nuevo"] 
            }
            for i, p in enumerate(scraped)
        ]

        response = post_results_to_appian(payload)
        print(response)
        return

    if not args:       
        products = get_product_map()
        print(products)
        return

    print("Uso incorrecto")
    print("python main.py")
    print("python main.py upgrade")


if __name__ == "__main__":
    main()
