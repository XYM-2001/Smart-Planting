from main.models import Product
import math


def get_product(page):
    product_all_list = Product.objects.all()
    product_list = []
    promotion_product_list = []
    for product in product_all_list:
        if product.isPromotion:
            if len(promotion_product_list) < 3:
                promotion_product_list.append(product)
        else:
            if not product.isVR:
                product_list.append(product)

        #if len(product_list) >= 10:
            #break

    page_num = max(1, math.ceil(len(product_list) / 8))
    page = min(page_num, page)
    product_list = product_list[page * 8 - 8: max(page * 8 - 1, len(product_list) - 1)]

    pagination = {'current': page, 'previous': True, 'previous_page': page - 1, 'next': True, 'next_page': page + 1,
                  'left': [], 'right': page_num}
    if page == 1:
        pagination['previous'] = False
        pagination['left'].append(1)
        if page_num > page:
            pagination['left'].append(2)
            if page_num == 2:
                pagination['right'] = 0
    else:
        pagination['left'].append(page - 1)
        pagination['left'].append(page)
    if page == page_num:
        pagination['next'] = False

    for product in product_list:
        product.zeroRating = range(5 - product.rating)
        product.rating = range(product.rating)
    
    if len(promotion_product_list) > 0:
        first_promotion_product = promotion_product_list.pop()
    else:
        first_promotion_product = None
    return product_list, promotion_product_list, first_promotion_product, pagination


def get_VR_FT(page):
    product_all_list = Product.objects.all()
    product_list = []
    VR_product_list = []
    for product in product_all_list:
        if product.isVR:
            VR_product_list.append(product)
        else:
            if not product.isPromotion:
                product_list.append(product)

        #if len(product_list) >= 10:
            #break

    page_num = math.ceil(len(product_list) / 8)
    page = min(page_num, page)
    product_list = product_list[page * 8 - 8: max(page * 8 - 1, len(product_list) - 1)]

    pagination = {'current': page, 'previous': True, 'previous_page': page - 1, 'next': True, 'next_page': page + 1,
                  'left': [], 'right': page_num}
    if page == 1:
        pagination['previous'] = False
        pagination['left'].append(1)
        if page_num > page:
            pagination['left'].append(2)
            if page_num == 2:
                pagination['right'] = 0
    else:
        pagination['left'].append(page - 1)
        pagination['left'].append(page)
    if page == page_num:
        pagination['next'] = False

    for product in product_list:
        product.zeroRating = range(5 - product.rating)
        product.rating = range(product.rating)

    first_promotion_product = VR_product_list.pop()

    return product_list, VR_product_list, first_promotion_product, pagination
