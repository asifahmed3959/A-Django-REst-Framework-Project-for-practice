from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuoteListSerializer
from .serializers import PublicationModelSerializer
from .serializers import ApprovedMemberSerializer

from base.models import Quote
from base.models import Publication
from base.models import ApprovedMembers

from django_filters.rest_framework.backends import DjangoFilterBackend

from .filters import ApprovedMembersFilter
from .filters import QuoteFilter

from .permissions import HasThisViewScope


class ApprovedMemberViewSet(viewsets.ModelViewSet):
    serializer_class = ApprovedMemberSerializer
    permission_classes = [IsAuthenticated,]
    queryset = ApprovedMembers.objects.all()
    lookup_field = 'pk'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ApprovedMembersFilter

    def get_queryset(self):
        return self.queryset.filter(quote__id=self.kwargs.get('quote_pk'))


class QuoteModelViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteListSerializer
    queryset = Quote.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,HasThisViewScope,]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuoteFilter
    scopes = ['quote.read','quote.write','quote.update','quote.delete']


class PublicationModelViewSet(viewsets.ModelViewSet):
    serializer_class = PublicationModelSerializer
    queryset = Publication.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated,]

    def filter_queryset(self, queryset):
        return queryset.filter(quote__id=self.kwargs.get('quote_pk'))


# class DashBoardViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny, ]
#
#     def list(self, request, format = None):
#         username = request.query_params.get('username')
#         text = request.query_params.get('text')
#         if username is not None:
#             queryset = Quote.objects.filter(author__username=username)
#             serializers = QuoteListSerializer(queryset, many=True)
#             return Response(serializers.data, status=status.HTTP_200_OK)
#         if text is not None:
#             queryset = Quote.objects.filter(quote__icontains=text)
#             serializers = QuoteListSerializer(queryset, many=True)
#             return Response(serializers.data,status=status.HTTP_200_OK)
#         queryset = Quote.objects.all()
#         serializers = QuoteListSerializer(queryset, many=True)
#         return Response(serializers.data, status=status.HTTP_200_OK)
#
#     def create(self, request, format = None):
#         serializer = QuoteListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(created_by=request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self,request,pk=None,format=None):
#         queryset = get_object_or_404(Quote, id = pk)
#         serializers = QuoteListSerializer(queryset)
#         return Response(serializers.data, status=status.HTTP_200_OK)
#
#     def update(self,request,pk=None,format=None):
#         quote = get_object_or_404(Quote, id=pk)
#         serializer = QuoteListSerializer(quote,request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(updated_by=request.user)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_200_OK)
#
#     def destroy(self,request, pk=None, format=None):
#         quote = get_object_or_404(Quote, id=pk)
#         quote.delete()
#         return Response(status=status.HTTP_200_OK)
#
#
#
# class PublicationViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny, ]
#
#     def list(self, request,quote_pk=None, format = None):
#         queryset = Publication.objects.filter(quote__id=quote_pk)
#         serializers = PublicationModelSerializer(queryset,many=True)
#         return Response(serializers.data, status=status.HTTP_200_OK)
#
#     def create(self, request, quote_pk = None, format = None):
#         serializer = PublicationModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self,request,quote_pk=None,pk=None,format=None):
#         queryset = get_object_or_404(Publication, id = pk)
#         serializers = PublicationModelSerializer(queryset)
#         return Response(serializers.data, status=status.HTTP_200_OK)
#
#     def update(self,request,quote_pk=None,pk=None,format=None):
#         publication = get_object_or_404(Publication, id=pk)
#         serializer = PublicationModelSerializer(publication,request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_200_OK)
#
#     def destroy(self,request, quote_pk=None,pk=None, format=None):
#         publication = get_object_or_404(Publication, id=pk)
#         publication.delete()
#         return Response(status=status.HTTP_200_OK)