from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,CreateAPIView,RetrieveUpdateAPIView,RetrieveDestroyAPIView

from posts.models import Post
from .serializers import PostListSerializer,PostDetailSerializer,PostCreateUpdateSerializer
from rest_framework.permissions import(
    AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
)
from .permissions import IsOwnerorReadOnly
class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abc'

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerorReadOnly]

    lookup_field = 'slug'
    def perform_update(self, serializer): #-- Changes the user from original user to updated user
        serializer.save(user=self.request.user)
    # lookup_url_kwarg = 'abc'

class PostDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    # lookup_url_kwarg = 'abc'