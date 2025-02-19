# Django

## Introduction
### How Django application works
    When ever an http request has been passed to the url. The request has been passed to appropriate view. The view will read or write data along with template it is displayed to user.
    URL - Http request uses URL Mapper to send data to corresponding view.
    View - A view receives Http request, access data via models and returns http request.
    Modals - Modals are python objects defining applications data structures. They also provide create, edit and query records in the database.
    Template - Templates define the structure of a file layout to represent data in the web page.
    An application aka app is the functional unit of the project. To create a app within the project we use the command
    python manage.py startapp poll
    this will create a application named poll with the skeleton folder structure to represent all the framework elements.
    Django clients - facebook, instagram, bitbucket, pinterest.
### How django urls works
    Django follows the following algorithm to serve any user request.
        Determine the root URLconf module to use.
        Load the Python module urls and look for the variable urlpatterns.
        Check each URL pattern in order, and stop at the first pattern match.
    Based on the pattern match, call the corresponding view with the following arguments:
        HttpRequest instance
        Named groups or positional arguments
        Keyword arguments
    Error handling views are called if no URL pattern matches, or if an exception is raised.
### URL patterns
    In the urlpattern each pattern is written using path or re_path functions.
    angled patterns are used to capture a value from the url
        apps/<int:age>/
    Captured values can be converted to string or other datatypes like int or slug.
    Upon a url match with the corresponding view function is called to action.
    apps/2018/, views.2018_view
    apps/<int:year>/, views_second_view
    2018_view is the first matched view this will be called.
    Convert this url to pattern match url
        apps/2018/02/hello world/
        apps/<int:year>/<int:month>/<slug:slug>/
    consider a user request app/201888/ technically it is wrong.
    we can use python regular expressions using re_path function
        syntax:
            (?P<name>Pattern)
            (?P<year>[0-9]{4})
            Use case:
                article/(?P<year>[0-9]{4})/
                only article/2018/ valid article/201888/ invalid
    Type converstions are not allowed all the values are sent as the strings
### Reversing the url
    Views using a custom Python function reverse
    Templates using the url template tag
    Model instances using get_absolute_url method.
### API - Application Programming Interface
    It is a set of protocals and tools that allows different applications to communicate each other. Apis enables us to create a complex applications by leveraging existing functionalities.
    Private APIs - within org, Partnered - Business, Public - 3rd party developer
    Since we are communicating with different application we need a common language that is JSON, or xml
### Urls in the django
    https://amazon.com/movies/reviews/

    Base Url : https://amazon.com/
    endpoint: movies/reviews

    Different kinds of urls
    https://amazon.com/movies/127/
    https://amazon.com/movies/127/reviews/
    https://amazon.com/movies/127/reviews/?limt=20
### Rest Api
    Representational State Transfer
    Rest is an architectural style.  
    Fouses on 1)endpoints 2)Methods(CRUD) - Create(Post), Read(Get), Update(Put), Delete(Delete) 3)headers 4)data
### Why do we need virtual enviroment
    Virtual evironment is a isolated environment where we can install multiple packages to run the application without installing in the system.
    Suppose I need iam working in project 1 where i require python 2.1 and pandas to run the application i need to create virtual env 1
    if i want to work on other project 2 where i require python 3.7 i can use this in virtual env 2
## Create Modal in django
    from django.db import models
    class Movie(models.Model):
        name = models.CharField(max_length=30)
        description = models.TextField(max_length=200)
        active = models.BooleanField(default=True)

        def __str__(self):
            return self.name
    Register in the admin
    from django.contrib import admin
    from .models import Movie
    admin.site.register(Movie)
    I can see the admin the browser http://localhost:8000/admin/
## Creating a view using JsonResponse
    from django.http import JsonResponse
    from .models import Movie
    class MoviesList(request):
        movies = Movies.objects.all()
        return JsonResponse({"movies":list(movies.values())}) # since JsonResponse require dictonary we have converted queryset to normal set and made key value pair

    In the urls add this
    urlpatterns = [
        path("movies/", movie_list, name="list-movies")
    ]
## How queryset works
    queryset is a special type of list that is used by django for faster retrival.
    movies = Movie.objects.all()
        Querset [<Movie:RRR>, <Movie:Kalki>]
        Since we have used self.name as return for __str__ during database creation
    movies = Movie.objects.all().values()
        Queryset [{name:"RRR", description:"Hello", active:true}, {...}]
    Convert queryset to normal list
    data = list(Movie.objects.all().values())

    How filter or get method works
    movie = Movie.objects.all().filter(name=name).first()
        # Now movie is not query set it is an object if i want to pass to JsonResponse i need to make it as dictionary
    data = {"name":movie.name, "description":movie.description, "active":movie.active}
# Sample CRUD operation on user table with serializers
    code in the view file
    class UserData(APIView):
        permission_classes = []
        authentication_classes = []
    
        def get(self, request):
            user_data = User.objects.all().values()
            return Response({"message": user_data})
    
        def post(self, request):
            username = request.data.get("username", None)
            password = request.data.get("password", None)
            name = request.data.get("name", None)
            email = request.data.get("email", None)
    
            if not username:
                return Response({"error": "Please enter username"}, status=400)
            if not password:
                return Response({"error": "please enter password field"}, status=400)
    
            user_obj = User.objects.create(username=username, name=name, email=email)
            user_obj.set_password(password)
            user_obj.save()
    
            return Response({"message": "Created User"}, status=201)
    
        def put(self, request):
            username = request.data.get("username", None)
            password = request.data.get("password", None)
            name = request.data.get("name", None)
            email = request.data.get("email", None)
    
            if not username:
                return Response({"error": "Please enter username"}, status=400)
            if not password:
                return Response({"error": "please enter password field"}, status=400)
    
            try:
                user_obj = User.objects.get(username=username)
                user_obj.username = username
                user_obj.name = name
                user_obj.email = email
                user_obj.set_password(password)
                user_obj.save()
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=404)
    
            return Response({"message": "Updated user successfully"}, status=200)
    
        def delete(self, request, username=None):
            if not username:
                return Response({"error": "please pass username from params"}, status=400)
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                return Response({"error": "User not found"}, status=404)
            user_obj.delete()
    
            return Response({"message": "deleted successfully"}, status=200)
    
    
    @api_view(["GET"])
    @authentication_classes([])
    @permission_classes([])
    def login(request):
    
        username = request.GET.get("username", None)
        password = request.GET.get("password", None)
    
        if not username or not password:
            return Response({"error": "Enter username and password"})
    
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            return Response({"error": "Username doesnot exist"})
        user_obj.check_password(password)
    
        return Response({"message": "Logged in successfully"}, status=200)
    Code in the url folder:
        path("userdata/", UserData.as_view(), name="userdetails"),
        path("userdata/<str:username>/", UserData.as_view(), name="individual_userdetails"),

    
## Serialization
### Why we need serialization
    To convert complex datastructures to python native and then to json
    Earlier we used to convert querysets into dictionaries and later i need to send it as json
    Instead of the manual work we can use serializer that reduces our work
    ![image](https://github.com/user-attachments/assets/c819d8b7-b796-4037-9440-88d0095bd869)
### Types of Serializers and views
    Serializers -
        serializers.Serializer
        serializers.ModelSerializer
    views - 
        function views
        class based views
            Generic Views
            Mixins
            Concrete View Classes
            ViewSets
#### serializers.Serializer
    from rest_framework import serializers

    class MovieSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField()
        description = serializers.CharField()
        active = serializers.BooleanField()
    How to use ?
    in the views file add this
    Code:
        class Movies(APIView):
            def get(self, request, name=None):
                if name is not None:
                    movies = Movie.objects.all().filter(name=name).first()
                    if movies is None:
                        return Response({"error": "No movie with the title exists"})
                    serialized_movies = MovieSerializer(movies) # Passing complex data like queryset here iam passing object
                    return Response(serialized_movies.data) # Directly passing the value
        
                movies = Movie.objects.all()
                serialized_movies = MovieSerializer(movies, many=True) ## Dont forgot to add this for multiple values of the serializers
                return Response({"movies": serialized_movies.data})
#### Model Serializer
    Code:
    from rest_framework import serializers
    from .models import Movie
    
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ["id", "name", "description", "active"] or fields = "__all__" or exclude = ["id"]
    In the views usage there is no difference between serializer and model serializer
### CRUD operations and there serializers
    Serializers Code:
        from rest_framework import serializers
        from .models import Movie
        
        class MovieSerializer(serializers.ModelSerializer):
            class Meta:
                model = Movie
                fields = ["id", "name", "description", "active"]
            
            def create(self, validated_data):
                return Movie.objects.create(**validated_data)
            
            def update(self, instance, validated_data):
                instance.name = validated_data.get("name", instance.name)
                instance.description = validated_data.get("description", instance.description)
                instance.active = validated_data.get("active", instance.active)
                instance.save()
                return instance
    Views Code:
        class Movies(APIView):
        def get(self, request, name=None):
            if name is not None:
                movies = Movie.objects.all().filter(name=name).first()
                if movies is None:
                    return Response({"error": "No movie with the title exists"})
                serialized_movies = MovieSerializer(movies)
                return Response(serialized_movies.data)
    
            movies = Movie.objects.all()
            serialized_movies = MovieSerializer(movies, many=True)
            return Response({"movies": serialized_movies.data})
        
        def post(self, request):
            data = request.data
            serializer = MovieSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "Added movie successfully"}, 201)
        
        def put(self, request, name=None):
            if name is None:
                return Response({"error": "Please pass the updated movie name int the params"})
            movie = Movie.objects.all().filter(name=name).first()
            serializer = MovieSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message": "Updated Successfully", "data": serializer.data})
            else:
                return Response(serializer.errors)
        
        def delete(self, request, name=None):
            if name is None:
                return Response({"error": "Please pass the name to delete"})
            movie = Movie.objects.all().filter(name=name).first()
            if movie is None:
                return Response({"error": "Movie name doesnot exist"})
            movie.delete()
            return Response({"Message": "Deleted Successfully"})
### Validations in serializer
    Code:
        # Field level validation
        # Here naming convention is important validate_fieldname
        def validate_name(self, value):
            if(len(value)<2):
                raise serializers.ValidationError("Name is too short")
            return value
        
        # Object level validation
        def validate(self,data):
            if(data.get("name") == data.get("description")):
                raise serializers.ValidationError("name and description should not be same")
            return data
### Custom fields in serializer and entire serializer code
    Code:
        from rest_framework import serializers
        from .models import Movie
        
        class MovieSerializer(serializers.ModelSerializer):
            # Adding custom field that is not present in the model
            # Step1)
            len_name = serializers.SerializerMethodField()
        
            class Meta:
                model = Movie
                fields = ["id", "name", "description", "active", "len_name"]
            
            # step2) Adding functionality to custom field
            def get_len_name(self, object):
                return len(object.name)
            
            def create(self, validated_data):
                return Movie.objects.create(**validated_data)
            
            def update(self, instance, validated_data):
                instance.name = validated_data.get("name", instance.name)
                instance.description = validated_data.get("description", instance.description)
                instance.active = validated_data.get("active", instance.active)
                instance.save()
                return instance
            
            # Field level validation
            def validate_name(self, value):
                if(len(value)<2):
                    raise serializers.ValidationError("Name is too short")
                return value
            
            # Object level validation
            def validate(self,data):
                if(data.get("name") == data.get("description")):
                    raise serializers.ValidationError("name and description should not be same")
                return data
### Nested Relation in serializer
    Consider this example a streaming platform contains many movies but one movie can be on one platform
    Plaform - many movies
    Movie(watchlist) - one platform

    In the watchlist table platform is a foreign key given below is the model
    Code:
        class WatchList(models.Model):
            streamingplatform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist") # Related name is important
            title = models.CharField(max_length=50)
            description = models.CharField(max_length=200)
            active = models.BooleanField(default=True)
            created = models.DateTimeField(auto_now_add=True)
        
            def __str__(self):
                return self.title

    Now my question is how to get all the movies of the all platforms
    Example: amazon can have RRR, sahoo etc
    To get this we need to modify serializer of the Platform
    Code:
        class StreamPlatformSerializer(serializers.ModelSerializer):
            watchlist = WatchListSerializer(many=True, read_only=True) # same related name is used here
            class Meta:
                model = StreamPlatform
                fields = "__all__"
        Instead of getting entire object we can get only strings 
                watchlist = serializers.StringRelatedField(many=True, read_only=True) # To get only strings
                watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # To get only primary key
## Mixins
    Mixins are very popular to perform very common tasks.
    All we need is to provide a basic settings and we can use common methods and perform all this common tasks very quickly

## ORM in django
    Suppose i have a DesignMaster table that has project has foreign key relationship and RoofDesignMap is the many to many relation.
    Models for both the tables:
        class DesignMaster(BaseModel):
            design_number = models.CharField(max_length=50)
            project = models.ForeignKey(Project, on_delete=models.CASCADE)
            version = models.FloatField(null=True)
            is_completed = models.BooleanField(default=False, null=False)
            is_default = models.BooleanField(default=False, null=False)
            roof_details = models.ManyToManyField(
                "RoofMaster", through=RoofDesignMap, null=True
            )
            location = models.ForeignKey(
                Location, on_delete=models.CASCADE, related_name="location", null=True
            )
            is_deleted = models.BooleanField(default=False)
        
            class meta:
                db_table = "design_master"

        class Project(BaseModel):
            project_number = models.CharField(max_length=10, null=False, unique=True)
            project_name = models.CharField(max_length=50, null=False)
            is_deleted = models.BooleanField(default=False, null=False)
            design_status = models.BooleanField(default=True, null=False)
            home_owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
            default_design = models.ForeignKey(
                "DesignMaster",
                on_delete=models.CASCADE,
                null=True,
                related_name="default_design",
            )
        
            class Meta:
                db_table = "project_master"

    Queries with foreign Key relations:
        Q) Search based on project_name and return entire Design master row?
            DesignMaster.objects.filter(project__project_name="D-0001_JohnDoe878").values().first()
        Q) Filter using project_name in DesignMaster and return project data from the DesignMaster? (simply get the project from the desingMaster table)
            project_obj = DesignMaster.objects.select_related("project").filter(project__project_name="D-0001_JohnDoe878").first().project #Got project object
            print(project_obj.project_name)
        Q) Given design_number that is present in the DesignMaster retrive the project_obj?
            project_obj = DesignMaster.objects.filter(design_number="D-001").first().project
            project_obj.project_name
            Fail Cases:
            project_obj = DesignMaster.objects.filter(design_number="D-001").values().first().project #projectObj is only avaliable when the it is queryset here by using .values i have flatted the data into dictonaries now the projectObj is not avaliable
        Q) Extention to the above question get both designMaster object and projectObj
            design_obj = DesignMaster.objects.filter(design_number="D-001").first() #The only constraint is dont flatten it using values
            project_obj = design_obj.project
    Queries with many to many relationship:
        Q) Given DesignMaster and RoofMaster they are both having many to many relationship
        Q) Given Design_number find the all the associated roofsMaster rows?
            DesignMaster.objects.filter(design_number="D-093").first().roof_details.values() #This contains all the roofs associated in the form of list of dictnaries
            DesignMaster.objects.filter(design_number="D-093").first().roof_details.values_list("id") #This contains all the ids
        Q) extention to the above question, Give the pitch value of the first roof?
            first_roof = DesignMaster.objects.filter(design_number="D-093").first().roof_details.values().first()
            first_roof.get("pitch")
            For optimization we can use this
            first_roof = DesignMaster.objects.prefetch_related("roof_details").filter(design_number="D-093").first().roof_details.values().first() #roof_details is the key that connects the RoofMaster table
### Q (Complex queries)
    Q) Queries
        Since if we use .filter .filter that only performs only and operator, if i want to perform various filters i can use complex queries.
        from django.db.models import Q
        Project.objects.filter(Q(project_number="D-0020") | Q(project_number="D-0021") & Q(is_deleted=True)).values()
        Project.objects.filter(Q(project_number="D-0020") | (Q(project_number="D-0021") & Q(is_deleted=True))).values() 
        Project.objects.filter((Q(project_number="D-0020") | Q(project_number="D-0021")) & Q(is_deleted=True)).values()
    Q) F Expressions
        F expressions is the encapsulated sql of the database field.
        Using F expressions we can manuplate data in database
        Update multiple data at once
        Query:
            from django.db.models import F
            RoofMaster.objects.update(pitch=F("pitch")*10)
        Update Individual Row:
            roof = RoofMaster.objects.all().first()
            roof.pitch = F("pitch") + 2
            roof.save()
            RoofMaster.objects.all().values()

## ModelViewSet
    ModelViewSet simplifiles the boiler plate code by providing all the CRUD operations in it and it handles the routing as well
    we can override the any method using list, create, retrive, destroy, partial_update
    Step1) Create a serializer
    In the serializers.py file add this
        class UserSerializer(ModelSerializer):
            class Meta:
                model = User
                fields = ["username", "email", "id"]
    Step2) Create a view and add this
        ModelViewSet View needs two parameters one is queryset and serializer_class, permission_classes and authentication_classes are optional
        
        class UserData(ModelViewSet):
            queryset = User.objects.all()
            serializer_class = UserSerializer
            permission_classes = []
            authentication_classes = []
    Step3) Add this in the Urls
        from django.routers import DefaultRouter
        urlpatterns = []

        router = DefaultRouter()
        router.register("userdata")
        urlpatterns+=router.urls
    Step4) Check the urls in the postman
        Get - http://localhost:8000/users/userdata/
        individual Data - http://localhost:8000/users/userdata/1/
        post - " , body needed
        put - http://localhost:8000/users/userdata/1/, body needed
        delete - http://localhost:8000/users/userdata/1/
            

        
    
            
        
            


    
    
    
    
