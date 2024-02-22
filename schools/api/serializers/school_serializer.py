from rest_framework import serializers
from schools.models import School
from rest_framework.validators import UniqueTogetherValidator


class SchoolSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True,min_length=3,max_length=100)

    def validate_title(self, value):
        if not value.replace(' ','').isalnum():
            raise serializers.ValidationError("Title must contain only alphabets and spaces")
        
        return value

    class Meta:
        model = School
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=School.objects.all(),
                fields=['title',],
                message='Title must be unique'
            )
        ]

    def create(self, validated_data):
        school = School.objects.create(**validated_data)
        return school
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
