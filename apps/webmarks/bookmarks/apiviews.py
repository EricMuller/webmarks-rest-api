

from rest_framework import parsers
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView

from rest_framework.response import Response

from rest_framework.views import APIView
from webmarks.rest_auth.permissions import EverybodyCanAuthentication
from webmarks.bookmarks import models
from webmarks.bookmarks.serializers import IdSerializer


class seachNoteView(APIView):
    throttle_classes = ()
    permission_classes = (EverybodyCanAuthentication)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token})


class addFoldertoBookmark(UpdateAPIView, DestroyAPIView):
    """
    Add folder to Bookmark
    """
    querySet = models.Bookmark.objects.all()
    throttle_classes = ()
    permission_classes = (permissions.AllowAny,)
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = IdSerializer

    def delete(self, request, pk, id, *args, **kwargs):

        bookmark = models.Bookmark.objects.get(pk=pk)
        folder = models.Folder.objects.get(pk=id)

        bookmark.folders.remove(folder)
        bookmark.save()

        return Response({'result': 'OK'})

    def update(self, request, pk, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        folderId = serializer.validated_data['id']

        bookmark = models.Bookmark.objects.get(pk=pk)
        folder = models.Folder.objects.get(pk=folderId)

        bookmark.folders.add(folder)
        bookmark.save()

        return Response(serializer.data)


add_folder_bookmark_view = addFoldertoBookmark.as_view()
