# Defaults
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Third party
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from .serializers import PostSerializer, CommentSerializer
from posts.models import Post, Comment


class SetPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'


class AllPosts(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = SetPagination


class PostDetails(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_pk'


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        """ After authentication and before POST, check if author field value
        is User and Author"""

        # ID number, not a user object.
        user_id = request.POST.get('author')

        # If user has no Author, exception will raise.
        try:
            User.objects.get(id=user_id).author

            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(f'{e}', status=status.HTTP_400_BAD_REQUEST)


class PostUpdate(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, post_pk):
        # Cache the URL post_pk not integer error.
        try:
            int(post_pk)

            post = get_object_or_404(Post, pk=post_pk)
            user_author = User.objects.get(pk=request.user.id).author
            post_author = post.author

            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                # If user is the post author.
                if user_author.id == post_author.id:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response('User has no author',
                                    status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(f'{e}', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_pk):
        try:
            int(post_pk)

            post = get_object_or_404(Post, pk=post_pk)
            user_author = User.objects.get(pk=request.user.id).author
            post_author = post.author

            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                # If user is the post author.
                if user_author.id == post_author.id:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response('User has no author',
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        # PK is not an integer.
        except Exception as e:
            return Response(f'{e}', status=status.HTTP_400_BAD_REQUEST)


class PostDelete(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # Needed when call the default delete method.
    lookup_url_kwarg = 'post_pk'

    def delete(self, request, post_pk):
        try:
            int(post_pk)

            post = get_object_or_404(Post, pk=post_pk)
            user_author = User.objects.get(pk=request.user.id).author
            post_author = post.author

            # If user is the post author.
            if user_author.id == post_author.id:
                return super().delete(self)
            else:
                return Response('User has no author',
                                status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(f'{e}', status=status.HTTP_400_BAD_REQUEST)


class PostShowRelatedComments(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = SetPagination

    def get(self, request, post_pk):
        """ Override the default GET behavior to show only comments that
        related to the current post only."""

        try:
            int(post_pk)

            comments = Comment.objects.filter(post=post_pk)
            serializer = CommentSerializer(comments, many=True)
        except Exception as e:
            return Response(f'{e}', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


class PostAddComment(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def post(self, request, post_pk):
        # Auto populate post and commenter fields.
        data = {
            'post': post_pk,
            'commenter': request.user.id,
            'content': request.data.get('content')
        }
        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class PostUpdateComment(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, post_pk, comment_pk):
        try:
            int(comment_pk)
            int(post_pk)

            comment = get_object_or_404(Comment, pk=comment_pk)
            user_id = User.objects.get(username=request.user).id
            commenter_id = comment.commenter.id
            serializer = CommentSerializer(
                comment, data=request.data, partial=True)

            post_not_404 = get_object_or_404(Post, pk=post_pk)

            if serializer.is_valid() and post_not_404:
                # If user is the comment creator.
                if user_id == commenter_id:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response('Not the comment creator',
                                    status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(f'{e}', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_pk, comment_pk):
        try:
            int(comment_pk)
            int(post_pk)

            comment = get_object_or_404(Comment, pk=comment_pk)
            user_id = User.objects.get(username=request.user).id
            commenter_id = comment.commenter.id
            data = {
                'post': post_pk,
                'commenter': commenter_id,
                'content': request.data.get('content'),
            }
            serializer = CommentSerializer(comment, data=data)

            post_not_404 = get_object_or_404(Post, pk=post_pk)

            if serializer.is_valid() and post_not_404:
                # If user is the comment creator.
                if user_id == commenter_id:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response('Not the comment creator',
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(f'{e}', status=status.HTTP_404_NOT_FOUND)


class PostDeleteComment(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # Needed when call the default delete method.
    lookup_url_kwarg = 'post_pk'

    def delete(self, request, post_pk, comment_pk):
        try:
            # Raise error if the post_pk and comment_pk is integers
            int(post_pk)
            int(comment_pk)
            # Check if request post is exists.
            get_object_or_404(Post, pk=post_pk)

            commenter_id = Comment.objects.get(pk=comment_pk).commenter.id
            user_id = request.user.id

            # If commenter is the logged-in user.
            if commenter_id == user_id:
                return super().delete(self)
            else:
                return Response('Unauthorized!!', status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response(f'{e}', status=status.HTTP_400_BAD_REQUEST)


class SearchPosts(AllPosts):
    # NOTE: Home and Search page are similar, so I derived from AllPosts.
    # URL: api/?query=<text>

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query and not query.isspace():
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )


class FilterByCategory(AllPosts):
    # NOTE: Home and Search page are similar, so I derived from AllPosts.
    # URL: api/filter/<category>/

    def get(self, request, category=None):
        if category:
            posts = Post.objects.filter(categories__name__icontains=category)
            if posts:
                serializer = PostSerializer(posts, many=True)
                return Response(serializer.data)
            else:
                return Response('No related posts.', status.HTTP_204_NO_CONTENT)
