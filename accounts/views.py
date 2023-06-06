from django.shortcuts import render,redirect
from django.db.models import Sum
from django.contrib.auth.models import auth,User
from django.contrib import messages
from .models import propsale,sectora
from django.db import connection
from django.core import serializers
from django.http import JsonResponse
import xml.etree.ElementTree as ET
import os

def logout(request):
    auth.logout(request)
    return redirect('/acc/home/')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/acc/home/')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('/acc/register/')

    else:
        return render(request,'register.html')


def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        second_name=request.POST['second_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('/acc/register/')
        else:
            user=User.objects.create_user(email=email,first_name=first_name,last_name=second_name,username=username,password=password)
            user.save()
            user=auth.authenticate(username=username,password=password)
            
            auth.login(request,user)
            return redirect('/acc/home/')
    else:
        return render(request,'register.html')
    
def add_sale(request):
    if request.method == 'POST':
        print('Added')
        #user inputs
        s_name=request.POST.get('name')
        s_date=request.POST.get('date')
        s_price=request.POST.get('price')
        s_sector=request.POST.get('sector')
        s_street=request.POST.get('street')
        s_plotno=request.POST.get('plotno')
       

        #creating object for model
        s=propsale()
        s.seller=s_name
        s.date=s_date
        s.price=s_price
        s.sector=s_sector
        s.street=s_street
        s.plotnum=s_plotno
        s.plotid=0
        
        
        s.save()
        return redirect('/acc/sales/')

       
    return render(request,'acc/sales.html',{})

def home(request):

    return render(request,'home.html')


def plotfinder(request):

    return render(request,'plotfinder.html')

#remove prefix for GeoJSON
# def remove_geojson(geojson_string):
#     prefix = '{"type":"Feature","properties":{},"geometry":'
#     if geojson_string.startswith(prefix):
#         geojson_string = geojson_string[len(prefix):]
#     return geojson_string


# def pricefinder(request):
#     if request.method == "GET":
#         poly = request.GET.get('poly')
    
#     print(poly)
#     within=sectora.objects.raw("""SELECT * FROM accounts_sectora WHERE ST_Within(geom, ST_GeomFromGeoJSON('{poly}'))""")
#     #within=sectora.objects.all()
#     return render(request,'pricefinder.html',{'within':within})
def pricefinder(request):
    if request.method == "GET":
        poly = request.GET.get('poly')
    
    print(poly)
    
    query = """
    SELECT * 
    FROM accounts_sectora 
    WHERE ST_Within(geom, ST_GeomFromGeoJSON(%s))
    """
    
    
    # within=sectora.objects.raw(query)
    # print(within)
    return render(request, 'pricefinder.html')


def data(request):
    xml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'accounts', 'filters.xml')

    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Extract the filter options
    property_types = [option.text for option in root.findall("./property_type/option")]
    price_ranges = [option.text for option in root.findall("./price_range/option")]
    bedrooms = [option.text for option in root.findall("./bedrooms/option")]
    # Extract more filter options as needed

    d_type = request.GET.get('property_type')
    price = request.GET.get('price_range')
    loc= request.GET.get('bedrooms')

    return render(request,'data.html', {
        'property_types': property_types,
        'price_ranges': price_ranges,
        'bedrooms': bedrooms,'dtype':d_type,'price':price,'loc':loc
        # Pass more filter options as needed
    })





def sales(request):
    
    sales = propsale.objects.values('seller').annotate(total_sales=Sum('price'))

    # for sale in sales:
    #     label.append(sale.seller)
    #     data.append(sale.price)


    return render(request,'sales.html', {'sales': sales})

def get_data(request):
    if request.method == "GET":
        poly = request.GET.get('poly')
    
    print(poly)
    
    query = """
    SELECT * 
    FROM accounts_sectora 
    WHERE ST_Within(geom, ST_GeomFromGeoJSON(%s))
    """
    
    within = sectora.objects.raw(query, [poly])
    
    # within=sectora.objects.raw(query)
    # within=sectora.objects.all()

    sdata = serializers.serialize('python', within)
    data = sdata[0]['fields'] if sdata else {}
    print(data)
    return JsonResponse(data)


