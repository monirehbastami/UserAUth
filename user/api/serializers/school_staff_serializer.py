from rest_framework import serializers
from user.models import SchoolStaffProfile, SchoolStaff, SchoolStaffProfile

class SchoolStaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolStaffProfile
        fields = ['school']


class SchoolStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolStaff
        fields = [
            'username',
            'email',
            'password',
            'phone_number'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        school_staff = super().create(validated_data)

        school_staff.set_password(password)
        school_staff.save()

        return school_staff