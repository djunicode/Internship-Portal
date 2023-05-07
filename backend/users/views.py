from django.shortcuts import render
from rest_framework.permissions import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView
from django.core.exceptions import PermissionDenied
from bs4 import BeautifulSoup
from urllib import request as req
import requests
import ssl
from urllib3 import poolmanager
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/internship-list/',
		'Detail View':'/internship-detail/<str:pk>/',
		'Create':'/internship-create/',
		'Update':'/internship-update/<str:pk>/',
		'Delete':'/internship-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def internshipList(request):
	Contacts = Internship.objects.all().order_by('-id')
	serializer = InternshipSerializer(Contacts, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def internshipDetail(request, pk):
	Contacts = Internship.objects.get(id=pk)
	serializer = InternshipSerializer(Contacts, many=False)
	return Response(serializer.data)

@api_view(['POST'])
def internshipCreate(request):
    serializer = InternshipSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def internshipUpdate(request, pk):
    Contacts = Internship.objects.get(id=pk)
    serializer = InternshipSerializer(instance=Contacts, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def internshipDelete(request, pk):
    Contacts = Internship.objects.get(id=pk)
    Contacts.delete()

    return Response('Item succsesfully deleted!')

#To display Research Project Lists to all students
class Research_ProjectList(ListAPIView):
    serializer_class = Research_ProjectSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Research_Project

#If a Professor wants to add Research Projects
class Research_ProjectLC(ListCreateAPIView):
    serializer_class = Research_ProjectSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        if self.request.user is Professor:
            try:
                user = self.request.user
                return Research_Project.objects.filter(professor=user)
            except:
                return Response({'status':403,'message': 'Some error has occured'})
        else:
            raise PermissionDenied
        
    def perform_create(self,serializer):
        if self.request.user is Professor:
            try:
                user = self.request.user
                print(user)
                serializer.save(professor=user)
                return Response(serializer.data)
            except:
                return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
        else:
            raise PermissionDenied

#If a Professor wants to update or delete a Research Project under him/her        
class Research_ProjectRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = Research_ProjectSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        if self.request.user is Professor:
            try:
                user = self.request.user
                return Research_Project.objects.filter(professor=user)
            except:
                return Response({'status':403,'message': 'Some error has occured'})
        else:
            raise PermissionDenied        

#web scrapping HelloIntern (login mandatory)
class HelloIntern(APIView):
    def get(self,request):
        try:
            url = "https://www.hellointern.com/search/"
            class TLSAdapter(requests.adapters.HTTPAdapter):

                def init_poolmanager(self, connections, maxsize, block=False):
                    ctx = ssl.create_default_context()
                    ctx.set_ciphers('DEFAULT@SECLEVEL=1')
                    self.poolmanager = poolmanager.PoolManager(
                            num_pools=connections,
                            maxsize=maxsize,
                            block=block,
                            ssl_version=ssl.PROTOCOL_TLS,
                            ssl_context=ctx)

            session = requests.session()
            session.mount('https://', TLSAdapter())
            html_text=session.get(url).text
            soup=BeautifulSoup(html_text,'lxml')
            content=soup.find_all('tr',class_='content')
            intern={}
            i=1
            for content in content:
                components={}
                title=content.find_all('a')[0].text.replace(' ','')
                company_name=content.find_all('a')[1].text.replace(' ','')
                day=content.find('span',class_='day').text.replace(' ','')
                month_year=content.find('span',class_='month_year').text.replace(' ','')
                salary=content.find('span',class_='salary_span').text.replace(' ','')
                start_date=content.find_all('b')[0].text.replace(' ','')
                location=content.find('span',class_='location_span').text.replace('\r\n ','').replace(' ','')
                end_date=content.find_all('b')[1].text.replace(' ','')
                components={'title':title,'company_name':company_name,'date_of_posting':day+month_year,'salary':salary,'internship_start_date':start_date,'internship_end_date':end_date,'location':location}
                intern.update({i:components})
                i=i+1
            return JsonResponse(intern)
        except:
            return JsonResponse({'status':403,'message': 'Some error has occured'})


def Internshala_scraper(final_url, pages):
    page_no = 1
    DataList = []
    while page_no <= pages:
        response = req.urlopen(final_url + str(page_no))
        soup = BeautifulSoup(response, "html.parser")
        internships = soup.findAll('h3', {'class': 'heading_4_5 profile'})

        for internship in internships[:15]:
            link = 'https://internshala.com/' + internship.findChildren("a",class_="view_detail_button")[0].get('href')
            Response = req.urlopen(link)
            Soup = BeautifulSoup(Response, "html.parser")
            Name = Soup.find('span', {'class': 'profile_on_detail_page'}).text.strip()
            Location = Soup.find('a', {'class': 'location_link view_detail_button'}).text.strip()
            Duration = Soup.find('div', {'class': 'other_detail_item_row'}).findChildren('div', {'class': 'other_detail_item'})[1].find('div', {'class': 'item_body'}).text.strip()
            Stipend = Soup.find('div', {'class': 'other_detail_item stipend_container'}).findChildren('div', {'class': 'item_body'})[0].find('span', {'class': 'stipend'}).text.strip()
            About = Soup.find('div', {'class': 'text-container about_company_text_container'}).text.strip()
            data = {
                'name': Name,
                'link': link,
                'location': Location,
                'duration': Duration,
                'stipend': Stipend,
                'about': About,
                    }
            DataList.append(data)
        page_no = page_no + 1
    return DataList

#To get proper url if body exists for Internshala view
def URL(body, url):
    if body['Category']:
        Category = body['Category']
        url = url + "-" + Category.replace(" ", "-").lower() + "-internships"
    else:
        url = url + "-internships"
    if body['Location']:
        Location = body['Location']
        url = url + "-in-" + Location.replace(" ", "-").lower()
    if body['Stipend']:
        Stipend = body['Stipend']
        url = url + "/stipend-" + str(Stipend) 
    return url

def InternShala(request):
    pages = 1
    url = "https://internshala.com/internships/work-from-home"

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if body:
        final_url = URL(body, url)
    else:
        final_url = url
    final_url = final_url + "/page-"
    print(final_url)
    DataList = Internshala_scraper(final_url, pages)

    return HttpResponse(DataList)