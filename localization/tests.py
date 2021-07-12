from django.test import TestCase

# Create your tests here.

"""


j = 0
        for title_title in title_title_list:
            product_details = ProductDetails(title=title_title, title_details=title_details_list[j],
                                             product_id=product)
            product_details.save()
            j = j + 1

        for about in about_title_list:
            product_about = ProductAbout(title=about, product_id=product)
            product_about.save()

product_details = ProductDetails.objects.filter(product_id=product_id)
product_about = ProductAbout.objects.filter(product_id=product_id)


update

j = 0
        for title_title in title_title_list:
            detail_id = details_ids[j]
            if detail_id == "blank" and title_title != "":
                Products_details = ProductDetails(title=title_title, title_details=title_details_list[j],
                                                  Product=Products)
                Products_details.save()
            else:
                if title_title != "":
                    Products_details = ProductDetails.objects.get(id=detail_id)
                    Products_details.title = title_title
                    Products_details.title_details = title_details_list[j]
                    Products_details.Products_id = Products
                    Products_details.save()
            j = j + 1

        k = 0
        for about in about_title_list:
            about_id = about_ids[k]
            if about_id == "blank" and about != "":
                Products_about = ProductAbout(title=about, Products_id=Products)
                Products_about.save()
            else:
                if about != "":
                    Products_about = ProductAbout.objects.get(id=about_id)
                    Products_about.title = about
                    Products_about.Products_id = Products
                    Products_about.save()
            k = k + 1

"""