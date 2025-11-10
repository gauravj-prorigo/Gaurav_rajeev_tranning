from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Blog,person
from .forms import BlogForm
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerialize ,TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthenticatedUser, IsEmployee, IsAdmin

# Create your views here.

def homepage(request):
    return render(request, 'home/home.html')


def Student(request):
    return


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


def create_blog(request):
    
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('blog_list') 
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})


def edit_blog(request,id):
    blog = get_object_or_404(Blog,id=id)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)    
        
    return render(request,'create_blog.html',{'form':form})  


def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == "POST":
        blog.delete() 
        return redirect('blog_list')
    return render(request, 'delete_blog.html', {'blog': blog})



@api_view(['GET'])
def index(request):
    courses = {
        'course_name' : 'python',
        'learn' : ['flask','Django','FastApi'],
        'course_provider' : 'Scalaer'
    }
    return Response(courses)

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person_api(request):
    if request.method == 'GET':
        objs = person.objects.all()
        serializers = peopleserilazers(objs,many = True)
        return Response(serializers.data)
    
    
    elif request.method == 'POST':
         data = request.data
         serializers = peopleserilazers(data = data)
         if serializers.is_valid():
             serializers.save()
             return Response(serializers.data)
         
         return Response(serializers.errors) 
     
     
    elif request.method == 'PUT':
         data = request.data
         obj = person.objects.get(id = data['id'])
         serializers = peopleserilazers(obj,data = data)
         if serializers.is_valid():
             serializers.save()
             return Response(serializers.data)
         
         return Response(serializers.errors) 
     
     
    elif request.method == 'PATCH':
         data = request.data
         obj = person.objects.get(id = data['id'])
         serializers = peopleserilazers(obj ,data = data , partial = True)
         if serializers.is_valid():
             serializers.save()
             return Response(serializers.data)
         
         return Response(serializers.errors) 
     
    else:
         data = request.data 
         obj = person.objects.get(id = data['id'])
         obj.delete()
         return Response({'Meassage': 'Person is deleted'})
    
    
# @api_view(['GET','POST'])
# def Blog_api(request):
#     if request.method == 'GET':
#         obj = Blog.objects.all()
#         serializers = blogserilazers(obj,many = True)
#         return Response(serializers.data)
    
#     else:
#         data = request.data
#         serializers = blogserilazers(data = data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
        
#         return Response(serializers.errors)       
    
    
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = blogserilazers
    permission_classes = [IsAuthenticated]  # default

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # everyone logged in can view
            return [IsAuthenticatedUser()]
        elif self.action == 'create':
            # employee or admin can create
            return [IsEmployee() | IsAdmin()]
        elif self.action in ['update', 'partial_update']:
            # only admin can edit
            return [IsAdmin()]
        elif self.action == 'destroy':
            # only admin can delete
            return [IsAdmin()]
        else:
            # fallback
            return [IsAuthenticated()]
    
    
    
    
def get_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        
class RegisterView(APIView):
     permission_classes = [AllowAny]
     def post(self,request):
         serializers = RegisterSerializer(data=request.data)
         if serializers.is_valid():
             user = serializers.save()
             tokens = get_token_for_user(user)
             return Response({"user": serializers.data, "tokens":tokens})
         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
     
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerialize(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_token_for_user(user)
            return Response({"user": user.username, "tokens": tokens})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
     
     


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
     