# Django

## Introduction
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
    




    
    
    
    
