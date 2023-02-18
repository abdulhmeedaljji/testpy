from django.shortcuts import render
from  store.models import Products
# Create your views here.



def Home(request):

    return render(request,"store/index.html")


def Payment(request):
    return render(request,"store/payment.html")




import requests

def send_to_telegram(message):

    apiToken = '5850535001:AAGaeeFzh0V4_7oit7Jbjilt359EtLe0RLU'
    chatID = '727117894'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)






def store(request):
    if request.method == 'POST':
        myStopWords = stopwords.words('english')
        lands = getLandsForSearch(request)
        searched = request.POST['searched']
        splitSearch = searched.split()
        print(splitSearch)
        products1 = Product.objects.all()
        listName = []
        for product1 in products1:
            nameSplit = product1.name.split()
            for sS in splitSearch:
                if sS in myStopWords:
                    break
                else:        
                    for nS in nameSplit:
                        if sS == nS:
                            print(nS)
                            listName.append(product1.name)
                            break
        for l in listName:
            print(l)
        products2 = Product.objects.filter(name__in = listName)
        print("GOOD")
        print(products2)
        products = Product.objects.filter(name__in = listName)
        for sS in splitSearch:
            allSearchs = Search.objects.filter(name = sS)
            length = len(allSearchs)
            if length > 0:
                search = Search.objects.filter(name=sS)
                for s in search:
                    s.count += 1
                    s.save()
            else:
                search = Search()
                search.lands = ""
                for land in lands:
                    search.lands = search.lands + " " + land.plant
                search.name = sS
                search.count += 1
                search.save()
    else: 
        products = Product.objects.all()
        searched = ''
    if request.user.is_authenticated:
        user = request.user.id
        order = Order.objects.filter(customer=user, complete=False)
        forder = order[0]
        items = OrderItem.objects.all()
    else:
        items = []
        order={"get_cart_total":0, "get_cart_items":0}
    print(Search.objects.order_by('-count')[:2])
    categories = Category.objects.all()
    context = {'categories':categories, 'products':products, 'items':items, 'forder':forder, 'searched':searched}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        user = request.user.id
        order = Order.objects.filter(customer=user, complete=False)
       # forder = order[0]
        items = OrderItem.objects.all()
    else:
        items = []
        order={"get_cart_total":0, "get_cart_items":0}
    context = {
        'items':items,
        #'forder':forder
    }
    # for orderr in order:
    #     print(orderr.transaction_id)
    return render(request, 'store/cart.html',  context)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user.id
        order = Order.objects.filter(customer=user, complete=False)
        forder = order[0]
        items = OrderItem.objects.all()
    else:
        items = []
        order={"get_cart_total":0, "get_cart_items":0}
    context = {
        'items':items,
        'forder':forder
    }
    # for orderr in order:
    #     print(orderr.transaction_id)
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added",  safe=False)
