from webmarks.bookmarks.apiviews import add_folder_bookmark_view
from webmarks.bookmarks import viewsets
from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

apiRouter = routers.DefaultRouter()
apiRouter.register(r'folders', viewsets.FolderViewSet)
apiRouter.register(r'bookmarks', viewsets.BookmarkViewSet)
apiRouter.register(r'tags', viewsets.TagViewSet)
apiRouter.register(r'archives', viewsets.ArchiveViewSet, base_name='archive')
# apiRouter.register(r'search', viewsets.SearchViewSet)
# apiRouter.register(r'upload', viewsets.FileUploaderViewSet)
# apiRouter.register(r'crawler', viewsets.CrawlerViewSet, base_name='crawler')
# apiRouter.register(r'archive', viewsets.ArchiveViewSet, base_name='archive')

urlpatterns = [
    # API V1
    url(r'v1/', include(apiRouter.urls, namespace='external_apis')),

    url(r'v1/bookmarks/(?P<pk>[\s\d\w().+-_,:&]+)/folders/$',
        add_folder_bookmark_view, name="add_folder_to_bookmark"),
    url(r'v1/bookmarks/(?P<pk>[\s\d\w().+-_,:&]+)/folders/(?P<id>[\s\d\w().+-_,:&]+)',
        add_folder_bookmark_view, name="add_folder_to_bookmark"),

]
