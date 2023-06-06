from django.shortcuts import render
from rest_framework.permissions import *
# Create your views here.
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
import requests
import ssl
from urllib3 import poolmanager
import certifi
from IPython.display import HTML
import re
from concurrent.futures import ThreadPoolExecutor

class InternshipList(APIView):
    def get(self, request):
        Contacts = Internship.objects.all()
        serializer = InternshipSerializer(Contacts, many=True)
        return Response(serializer.data)
    def post(self, request):
        pass

class InternshipDetail(APIView):
    def get(self, request, pk):
        Contacts = Internship.objects.get(id=pk)
        serializer = InternshipSerializer(Contacts, many=False)
        return Response(serializer.data)
    def post(self):
        pass

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
            
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(scrape_url, url) for url in urls]
                
                for future in futures:
                    results = future.result()
                    for result in results:
                        intern[i] = result
                        i += 1
            
            return Response(intern)
        
        except:
            return JsonResponse({'status': 403, 'message': 'Some error has occurred'})