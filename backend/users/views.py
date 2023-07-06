from rest_framework.permissions import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView
from django.core.exceptions import PermissionDenied
from bs4 import BeautifulSoup
from urllib import request as req
import requests
import ssl
from urllib3 import poolmanager
import certifi
import re
from concurrent.futures import ThreadPoolExecutor
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
        if self.request.user.type == 'PROFESSOR':
            try:
                user = self.request.user
                return Research_Project.objects.filter(professor=user)
            except:
                return Response({'status':403,'message': 'Some error has occured'})
        else:
            raise PermissionDenied
        
    def perform_create(self,serializer):
        print(self.request.user is Professor)
        if self.request.user.type == 'PROFESSOR':
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
        if self.request.user.type == 'PROFESSOR':
            try:
                user = self.request.user
                return Research_Project.objects.filter(professor=user)
            except:
                return Response({'status':403,'message': 'Some error has occured'})
        else:
            raise PermissionDenied



#webscrapping linkedin (300 internships approx)
class LinkedIn(APIView):
    def get(self, request):
        try:
            urls = [
                   "https://in.linkedin.com/jobs/business-analytics-intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/cloud-intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/front-end-development-internship-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/web-development-intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/developer-internship-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/reactjs-interns-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/intern-react-js-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/react-js-developer-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/react-js-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/ux-design-intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/ui-design-intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/python-django-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/node-js-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/node-js-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/node-js-developer-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/flutter-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/data-science-intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/data-science-intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/data-science-internship-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/machine-learning-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/research-intern-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/iot-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/blockchain-intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/mechanical-internship-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/natural-language-processing-intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/finance-internship-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/intern-hr-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/hr-intern-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/marketing-internship-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/marketing-intern-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/marketing-intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/business-analyst-intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/technical-intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/technology-intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/internship-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/linkedin-internship-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/research-internship-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/summer-internship-jobs-mumbai-metropolitan-region?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/summer-intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/internship-jobs-maharashtra?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/summer-internship-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/internship-intern-jobs-thane?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/parttime-intern-jobs?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/summer-intern-jobs-mumbai?position=1&pageNum=0",
                   "https://in.linkedin.com/jobs/research-intern-jobs-mumbai-metropolitan-region?position=1&pageNum=0",

                    #add more linkedin static urls here
            ]
            
            intern = {}
            i = 1
            
            def scrape_url(url):
                try:
                    class TLSAdapter(requests.adapters.HTTPAdapter):
                        def init_poolmanager(self, connections, maxsize, block=False):
                            ctx = ssl.create_default_context(cafile=certifi.where())
                            ctx.set_ciphers('DEFAULT@SECLEVEL=1')
                            self.poolmanager = poolmanager.PoolManager(
                                num_pools=connections,
                                maxsize=maxsize,
                                block=block,
                                ssl_version=ssl.PROTOCOL_TLS,
                                ssl_context=ctx)
                    
                    headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
                    session = requests.session()
                    session.mount('https://', TLSAdapter())
                    html_text = session.get(url, headers=headers).text
                    soup = BeautifulSoup(html_text, 'lxml')
                    content = str(soup.find('ul', class_='jobs-search__results-list'))
                    soup = BeautifulSoup(content, 'lxml')
                    content = soup.find_all('li')
                    
                    results = []
                    for content in content:
                        try:
                            link = content.find('a', {'class': 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'}).get('href')
                        except:
                            link = 'information unavailable'
                        
                        try:
                            title = content.find('h3', class_='base-search-card__title').text.replace('\n      ', '')
                            cleanedtitle = re.sub(r'\s+', ' ', title)
                        except:
                            cleanedtitle = 'information unavailable'
                        
                        try:
                            company = content.find('a', class_='hidden-nested-link').text.replace('\n         ', '')
                            cleanedcompany = re.sub(r'\s+', ' ', company)
                        except:
                            cleanedcompany = 'information unavailable'
                        
                        try:
                            date_of_posting = content.find('time', {'class': 'job-search-card__listdate'}).get('datetime')
                        except:
                            try:
                                date_of_posting = content.find('time', {'class': 'job-search-card__listdate--new'}).get('datetime')
                            except:
                                date_of_posting = 'information unavailable'
                        
                        try:
                            location = content.find('span', class_="job-search-card__location").text.replace('\n         ', '')
                        except:
                            location = 'information unavailable'
                        
                        components = {'title': cleanedtitle, 'company_name': cleanedcompany, 'location': location, 'date_of_posting': date_of_posting, 'link': link}
                        results.append(components)
                    
                    return results
                except:
                    return []
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(scrape_url, url) for url in urls]
                
                for future in futures:
                    results = future.result()
                    for result in results:
                        intern[i] = result
                        i += 1
            
            return Response(intern)
        
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
