# from webmarks.rest_auth.permissions import DefaultsAuthentificationMixin
from webmarks.bookmarks import models
from webmarks.bookmarks import serializers
from webmarks.drf_utils.cache import CustomListKeyConstructor
from webmarks.storage.crawler import Crawler
from webmarks.storage.storage import FileStore
from webmarks.bookmarks.filters import BookmarkFilter
from webmarks.bookmarks.filters import FolderFilter
from webmarks.bookmarks.filters import TagFilter
from webmarks.drf_utils.viewsets import AggregateModelViewSet

# from webmarks.storage.models import Archive
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework import permissions
import base64
import logging
import uuid
stdlogger = logging.getLogger(__name__)


class FolderViewSet(AggregateModelViewSet):

    """
    retrieve:
        Return a Folder instance.

    list:
        Return all Folder instance , ordered by most recently created.

    create:
        Create a new Folder.

    delete:
        Remove an existing Folder.

    partial_update:
        Update one or more fields on an existing Folder.

    update:
        Update a Folder.
    """
    queryset = models.Folder.objects.all()
    serializer_class = serializers.FolderSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = FolderFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):

        return models.Folder.objects.filter(user_cre_id=self.request.user.id)

    @detail_route(methods=['get'])
    def bookmarks(self, request, pk):
        """
            Return all bookmarks of folder.
        """
        self.queryset = models.Bookmark.objects.filter(folders__in=[pk])

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = serializers.BookmarkSerializer(
                self.queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.BookmarkSerializer(self.queryset, many=True)
        return Response(serializer.data)


class BookmarkViewSet(AggregateModelViewSet):

    """
    retrieve:
        Return a Bookmark instance.

    list:
        Return all Bookmark instance , ordered by most recently created.

    create:
        Create a new Bookmark.

    delete:
        Remove an existing Bookmark.

    partial_update:
        Update one or more fields on an existing Bookmark.

    update:
        Update a Bookmark.
    """

    queryset = models.Bookmark.objects.prefetch_related('tags')
    serializer_class = serializers.BookmarkSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = BookmarkFilter
    permission_classes = (permissions.IsAuthenticated,)

    # .prefetch_related(
    #    'tags').prefetch_related('archive').values_list('title','rate')
    # queryset = models.Note.objects.prefetch_related('tags').values
    # ('archive__note', 'id', 'title', 'url', 'description', 'updated_dt', 'created_dt',
    # 'user_cre', 'user_upd', 'archived_dt', 'rate', 'type', 'status', 'public', 'schedule_dt')

    @cache_response(key_func=CustomListKeyConstructor())
    def list(self, *args, **kwargs):
        return super(BookmarkViewSet, self).list(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        # print('user_id=' + str(self.request.user.id))
        return models.Bookmark.objects.prefetch_related('tags').filter(
            user_cre_id=self.request.user.id)

    def get_serializer_class(self):
        # if self.action == 'list':
        #    return serializers.NoteListSerializer
        return serializers.BookmarkSerializer

    @detail_route(methods=['get'])
    def title(self, request, pk=None):
        """
            Return the title of url's Page Bookmark.
        """
        crawler = Crawler()

        stdlogger.debug(pk)
        url = base64.b64decode(pk)
        stdlogger.info(url.decode())
        crawler.crawl_title(url.decode())
        serializer = serializers.CrawlSerializer(crawler)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def archive(self, request, pk):
        """
            Archive the Bookmark Page.
        """
        bookmark = self.get_object()
        stdlogger.debug(pk)
        crawler = Crawler()
        # url = base64.b64decode(pk)
        # stdlogger.info(url.decode())
        crawler.crawl(bookmark.url)

        user = request.user

        FileStore().store(user.username, str(bookmark.uuid), crawler.html.encode())

        archive = models.Archive.create(
            bookmark, crawler.content_type, crawler.html.encode())
        archive.save()

        bookmark.archive_id = archive.id
        bookmark.save()
        serializer = serializers.ArchiveSerializer(archive)
        return Response(serializer.data)


class TagViewSet(AggregateModelViewSet):
    """
    retrieve:
        Return a Tag instance.

    list:
        Return all Tag instance , ordered by most recently created.

    create:
        Create a new Tag.

    delete:
        Remove an existing Tag.

    partial_update:
        Update one or more fields on an existing Tag.

    update:
        Update a Tag.
    """
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TagFilter
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(methods=['get'])
    def count(self, request):
        queryset = models.Tag.objects.with_counts(user_cre_id=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.TagCountSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serializer = serializers.TagCountSerializer(queryset, many=True)
        return Response(serializer.data)


class CrawlerViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk):
        crawler = Crawler()
        stdlogger.debug(pk)
        url = base64.b64decode(pk)
        stdlogger.info(url.decode())
        data = crawler.crawl(url.decode())
        serializer = serializers.CrawlSerializer(data)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def title(self, request, pk=None):
        crawler = Crawler()

        stdlogger.debug(pk)
        url = base64.b64decode(pk)
        stdlogger.info(url.decode())
        crawler.crawl_title(url.decode())
        serializer = serializers.CrawlSerializer(crawler)
        return Response(serializer.data)


class ArchiveViewSet(AggregateModelViewSet):

    """
    retrieve:
        Return a Archive instance.

    list:
        Return all Archives, ordered by most recently joined.

    create:
        Create a new Archive.

    delete:
        Remove an existing Archive.

    partial_update:
        Update one or more fields on an existing Archive.

    update:
        Update a Archive.
    """

    filter_backends = (filters.DjangoFilterBackend,)
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer

    # renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer,
    #                    renderers.StaticHTMLRenderer,)
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, pk, format=None):
        archive = get_object_or_404(models.Archive, pk=pk)
        if request.accepted_renderer.format == 'html':
            return Response(archive.data)

        serializer = self.serializer_class(archive)
        response = Response(serializer.data)
        response['Cache-Control'] = 'no-cache'
        return response

    @detail_route(methods=['get'])
    def download(self, request, pk):
        """
            Download Archive File.
        """
        archive = get_object_or_404(models.Archive, pk=pk)
        # tmp = tempfile.NamedTemporaryFile(suffix=".note")
        filename = archive.name.split('/')[-1]
        resp = HttpResponse(
            archive.data, content_type='application/text;charset=UTF-8')
        resp['Content-Disposition'] = "attachment; filename=%s" % filename
        return resp
