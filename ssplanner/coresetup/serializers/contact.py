from coresetup.models.contact import Contact
from rest_framework import serializers
from datetime import datetime


class ContactSerializer(serializers.ModelSerializer):
    """[summary]

    Args:
        serializers ([type]): [description]

    Returns:
        [type]: [description]
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    
    class Meta:
        model = Contact
        fields = '__all__'
    
    def update(self, instance, validated_data):
        """[summary]

        Args:
            instance ([type]): [description]
            validated_data ([type]): [description]

        Returns:
            [type]: [description]
        """
        instance.email = validated_data.get('email', instance.email)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.set_password(validated_data['password'])
        instance.is_active = True
        instance.save()
        return instance

    def create(self, validated_data):        
        contact = Contact(
            mobile_number=validated_data['mobile_number'],
            last_login=datetime.now(),
            email=validated_data['email'],
            user_name=validated_data['user_name'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=True,
            is_active=True,            
        )
        contact.set_password(validated_data['password'])
        contact.save()
        return contact


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            'id', 'user_name', 'mobile_number', 'last_login',
            'email', 'first_name',
            'last_name', 'registered_time',
            ]
