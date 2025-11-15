from rest_framework import viewsets, permissions

from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only see their own activities by default
        user = self.request.user
        return Activity.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
