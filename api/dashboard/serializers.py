from rest_framework import serializers
from rest_framework import status

from base.models import Quote
from base.models import Publication
from base.models import ApprovedMembers

from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','id','email','username']


class ApprovedMemberShortSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)
    class Meta:
        model = ApprovedMembers
        fields = ('user',)


class QuoteListSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True, required=True)
    created_on = serializers.DateTimeField(read_only=True)
    signed = AuthorSerializer(many=True,read_only=True)
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Quote
        fields = ['quote','author','created_on','author_id','id','created_by','updated_by','signed']


class PublicationModelSerializer(serializers.ModelSerializer):
    quote_id = serializers.UUIDField(write_only=True)
    quote = QuoteListSerializer(read_only=True)
    class Meta:
        model = Publication
        fields = ('name','date','quote', 'quote_id','id')


class ApprovedMemberSerializer(ApprovedMemberShortSerializer):
    quote_id = serializers.UUIDField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)
    quote = QuoteListSerializer(read_only=True)
    class Meta:
        model = ApprovedMembers
        fields = ('id','quote_id','user_id','underground_name','rank','user','quote')

    def validate(self, attrs):
        rank = attrs['rank']
        if rank>10 or rank < 0:
            raise serializers.ValidationError('value must be less than 10 and greater than 0',
                                              status_code=status.HTTP_409_CONFLICT)
        return attrs