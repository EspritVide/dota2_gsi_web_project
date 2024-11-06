import zipfile
from io import BytesIO

from django.http.response import FileResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GameSerializer, GameDetailSerializer
from games.models import Game


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.prefetch_related('players')
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = GameDetailSerializer
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(
            players__user=self.request.user
            ).order_by('datetime')


class CfgFileView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        path, file_content = request.user.get_cfg_file()
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zip_file:
            zip_file.writestr(path, file_content)
        buffer.seek(0)
        return FileResponse(
            buffer,
            content_type='application/zip',
            as_attachment=True,
            filename='gsi_web_cfg_file.zip', )
