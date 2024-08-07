# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer


class Sensors(ListAPIView):
    queryset = Sensor.objects.all().order_by('id')
    serializer_class = SensorSerializer

    def post(self, request):
        data = request.data
        Sensor.objects.create(name=data.get('name'), description=data.get('description'))
        return Response({'status': 'New sensor add'})

    def patch(self, request, id):
        data = request.data
        sensor = Sensor.objects.all().filter(id=id)[0]
        sensor.description = data.get('description')
        sensor.save()
        return Response('Sensor redeployed')


class Measurements(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request):
        data = request.data
        sensor = Sensor.objects.all().filter(id=data.get('sensor'))
        Measurement.objects.create(sensor=sensor[0], temperature=data.get('temperature'))
        # Measurement.objects.create(sensor=sensor[0], temperature=datda.get('temperature'),
        # image='https://www.rgo.ru/sites/default/files/node/73720/photo-2023-10-25-140017.jpeg')
        return Response({'status': 'New measurement add'})


class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
