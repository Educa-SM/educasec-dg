
from rest_framework import viewsets

class BaseViewSet(viewsets.ModelViewSet):
   def perform_create(self, serializer):
      serializer.save(creation_user=self.request.user)

   def perform_update(self, serializer):
      serializer.save(update_user=self.request.user)