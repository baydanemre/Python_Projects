import requests as r 
from bs4 import BeautifulSoup as bs 
import time

products = {}

dress = "https://www.trendyol.com/elbise-x-c56?pi="
tshirt = "https://www.trendyol.com/kadin-t-shirt-x-g1-c73?pi="
shirt = "https://www.trendyol.com/kadin-gomlek-x-g1-c75?pi="
jacket = "https://www.trendyol.com/kot-ceket-y-s12676?pi="
pants = "https://www.trendyol.com/kadin-pantolon-x-g1-c70?pi="
coat = "https://www.trendyol.com/kadin-mont-x-g1-c118?pi="
blouse = "https://www.trendyol.com/kadin-bluz-x-g1-c1019?pi="
overcoat = "https://www.trendyol.com/kadin-kaban-x-g1-c1075?pi="

search_term = input("Which products do you want to see: ")

def switch(search_term):
    if search_term == "dress".lower():
        return dress
    elif search_term == "tshirt".lower():
        return tshirt
    elif search_term == "shirt".lower():
        return shirt
    elif search_term == "jacket".lower():
        return jacket
    elif search_term == "pants".lower():
        return pants
    elif search_term == "coat".lower():
        return coat
    elif search_term == "blouse".lower():
        return blouse
    elif search_term == "overcoat".lower():
        return overcoat
    
for i in range(1,10):
    url = f"{switch(search_term)}{i}"
    page = r.get(url)
    soup = bs(page.content,"html.parser")

    product_infos = soup.find_all("div",class_="p-card-chldrn-cntnr card-border")

    for a in product_infos:
        before_discount = a.find("div",class_="prc-box-orgnl")
        after_discount = a.find("div",class_="prc-box-dscntd")
        try:
            product_name = a.find("span",class_="prdct-desc-cntnr-name hasRatings")
        except AttributeError:
            product_name = a.find("span",class_="prdct-desc-cntnr-name")  

        brand_name = a.find("span", class_="prdct-desc-cntnr-ttl")

        try:
            rating_count = a.find("span",class_="ratingCount")
            rating_count = rating_count.text.replace("(","").replace(")","")                
        except AttributeError:             
            rating_count = "0" 

        product_link = a.find("a")
        if before_discount != None and after_discount != None:
            before_price = before_discount.text.replace(" TL","")
            after_price = after_discount.text.replace(" TL","")

            product_id = product_name.get("title")

            if product_id not in products:
                products[product_id] = {
                "Product Name": product_name.get("title"),
                "Brand Name": brand_name.get("title"),
                "Rating Count": rating_count,
                "Original Price": before_price,
                "Discounted Price": after_price,
                "Product Link": f"https://www.trendyol.com{product_link.get('href').split('?')[0]}"
            }

best_discounted = list()
max_discount = 0.0

for product_id, features in products.items():
    for key, value in features.items():
        if key == "Original Price":
            original = float(value.split(",")[0])
        if key == "Discounted Price":
            discounted = float(value.split(",")[0])
    discount_percentage = f"{(original - discounted) * 100 / original:.1f}"
    best_discounted.append(discount_percentage)
    features["Discount Percentage"] = discount_percentage

# Display top 10 products with the highest discounts
sorted_products = sorted(products.items(), key=lambda x: float(x[1].get("Discount Percentage", 0)), reverse=True)

for product_id, features in sorted_products[:10]:
    print(f"Product ID: {product_id}")
    for feature, value in features.items():
        print(f"{feature}: {value}")
    print("\n")

            
        
