from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .api_client import RadarAPIClient


class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        client = RadarAPIClient()

        estadisticas = client.obtener_estadisticas()
        ultimas_mediciones = client.obtener_mediciones(limit=10)
        distancia = client.obtener_distancia()
        limite_velocidad = client.obtener_limite_velocidad()

        for medicion in ultimas_mediciones:
            velocidad = medicion.get('velocidad_kmh')
            medicion['exceso'] = velocidad and velocidad > limite_velocidad

        context = {
            'estadisticas': estadisticas,
            'ultimas_mediciones': ultimas_mediciones,
            'distancia_actual': distancia,
            'limite_velocidad': limite_velocidad,
        }
        return render(request, self.template_name, context)


class MedicionesListView(View):
    template_name = 'dashboard/mediciones_lista.html'

    def get(self, request):
        client = RadarAPIClient()

        page = int(request.GET.get('page', 1))
        limit = 20
        skip = (page - 1) * limit

        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        mediciones = client.obtener_mediciones(
            skip=skip,
            limit=limit,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        limite_velocidad = client.obtener_limite_velocidad()

        for medicion in mediciones:
            velocidad = medicion.get('velocidad_kmh')
            medicion['exceso'] = velocidad and velocidad > limite_velocidad

        context = {
            'mediciones': mediciones,
            'page': page,
            'has_prev': page > 1,
            'has_next': len(mediciones) == limit,
            'fecha_inicio': fecha_inicio or '',
            'fecha_fin': fecha_fin or '',
            'limite_velocidad': limite_velocidad,
        }
        return render(request, self.template_name, context)


class MedicionDetailView(View):
    template_name = 'dashboard/medicion_detalle.html'

    def get(self, request, pk):
        client = RadarAPIClient()
        medicion = client.obtener_medicion(pk)

        if 'error' in medicion:
            messages.error(request, 'Medicion no encontrada')
            return redirect('dashboard:mediciones')

        limite_velocidad = client.obtener_limite_velocidad()
        velocidad = medicion.get('velocidad_kmh')
        medicion['exceso'] = velocidad and velocidad > limite_velocidad

        context = {
            'medicion': medicion,
            'limite_velocidad': limite_velocidad,
        }
        return render(request, self.template_name, context)


class ReportesView(View):
    template_name = 'dashboard/reportes.html'

    def get(self, request):
        client = RadarAPIClient()

        estadisticas = client.obtener_estadisticas()
        mediciones = client.obtener_mediciones(limit=50)

        velocidades = []
        timestamps = []
        for m in reversed(mediciones):
            if m.get('velocidad_kmh'):
                velocidades.append(m['velocidad_kmh'])
                timestamps.append(m['timestamp'][:16].replace('T', ' '))

        context = {
            'estadisticas': estadisticas,
            'velocidades_json': velocidades,
            'timestamps_json': timestamps,
            'total_mediciones': len(mediciones),
        }
        return render(request, self.template_name, context)


class ConfiguracionView(View):
    template_name = 'dashboard/configuracion.html'

    def get(self, request):
        client = RadarAPIClient()
        distancia = client.obtener_distancia()
        limite_velocidad = client.obtener_limite_velocidad()

        context = {
            'distancia_actual': distancia,
            'limite_velocidad': limite_velocidad,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        client = RadarAPIClient()

        nueva_distancia = request.POST.get('distancia')
        if nueva_distancia:
            try:
                distancia = float(nueva_distancia)
                if distancia > 0:
                    result = client.actualizar_distancia(distancia)
                    if 'error' not in result:
                        messages.success(request, f'Distancia actualizada a {distancia} metros')
                    else:
                        messages.error(request, f'Error: {result["error"]}')
                else:
                    messages.error(request, 'La distancia debe ser mayor a 0')
            except ValueError:
                messages.error(request, 'Valor de distancia invalido')

        nuevo_limite = request.POST.get('limite_velocidad')
        if nuevo_limite:
            try:
                limite = float(nuevo_limite)
                if limite > 0:
                    result = client.actualizar_limite_velocidad(limite)
                    if 'error' not in result:
                        messages.success(request, f'Limite de velocidad actualizado a {limite} km/h')
                    else:
                        messages.error(request, f'Error: {result["error"]}')
                else:
                    messages.error(request, 'El limite debe ser mayor a 0')
            except ValueError:
                messages.error(request, 'Valor de limite invalido')

        return redirect('dashboard:configuracion')


class NuevaMedicionView(View):
    template_name = 'dashboard/nueva_medicion.html'

    def get(self, request):
        client = RadarAPIClient()
        distancia = client.obtener_distancia()
        limite_velocidad = client.obtener_limite_velocidad()
        hay_pendiente = client.hay_medicion_pendiente()

        # Estado: 'esperando_sensor1' (azul), 'esperando_sensor2' (naranja)
        estado = 'esperando_sensor2' if hay_pendiente else 'esperando_sensor1'

        context = {
            'distancia_actual': distancia,
            'limite_velocidad': limite_velocidad,
            'estado': estado,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        client = RadarAPIClient()
        accion = request.POST.get('accion')

        if accion == 'iniciar':
            result = client.registrar_medicion()
            if 'error' not in result:
                # Compatibilidad con API simple (mensaje) y API completa (es_primera_medicion)
                velocidad_kmh = result.get('velocidad_kmh')
                tiempo = result.get('tiempo_recorrido') or result.get('tiempo_segundos')

                if velocidad_kmh is not None and tiempo is not None:
                    # Medición completa
                    limite_velocidad = client.obtener_limite_velocidad()
                    if velocidad_kmh > limite_velocidad:
                        messages.warning(
                            request,
                            f'Medicion completada: {velocidad_kmh:.2f} km/h en {tiempo:.2f}s - EXCESO DE VELOCIDAD'
                        )
                    else:
                        messages.success(
                            request,
                            f'Medicion completada: {velocidad_kmh:.2f} km/h en {tiempo:.2f}s'
                        )
                else:
                    # Esperando segundo sensor
                    mensaje = result.get('mensaje', 'Sensor 1 activado. Esperando sensor 2...')
                    messages.info(request, mensaje)
            else:
                messages.error(request, f'Error al registrar: {result["error"]}')

        return redirect('dashboard:nueva_medicion')


class MedicionesAutoView(View):
    template_name = 'dashboard/mediciones_auto.html'

    def get(self, request):
        client = RadarAPIClient()
        distancia = client.obtener_distancia()
        limite_velocidad = client.obtener_limite_velocidad()
        hay_pendiente = client.hay_medicion_pendiente()

        estado = 'esperando_sensor2' if hay_pendiente else 'esperando_sensor1'

        ultimas_mediciones = client.obtener_mediciones(limit=5)
        for medicion in ultimas_mediciones:
            velocidad = medicion.get('velocidad_kmh')
            medicion['exceso'] = velocidad and velocidad > limite_velocidad

        api_url = getattr(settings, 'FASTAPI_BASE_URL', 'http://localhost:8080')

        context = {
            'distancia_actual': distancia,
            'limite_velocidad': limite_velocidad,
            'estado': estado,
            'ultimas_mediciones': ultimas_mediciones,
            'api_url': api_url,
        }
        return render(request, self.template_name, context)


class MedicionesAutoAPIView(View):
    """Endpoint para polling desde JavaScript - solo mediciones en tiempo real."""

    def get(self, request):
        from datetime import datetime, timedelta

        client = RadarAPIClient()
        hay_pendiente = client.hay_medicion_pendiente()
        limite_velocidad = client.obtener_limite_velocidad()

        # Solo obtener mediciones de los últimos 10 segundos (tiempo real)
        ahora = datetime.now()
        hace_10_segundos = ahora - timedelta(seconds=10)
        fecha_inicio = hace_10_segundos.strftime('%Y-%m-%dT%H:%M:%S')

        ultimas_mediciones = client.obtener_mediciones(
            limit=5,
            fecha_inicio=fecha_inicio
        )
        for medicion in ultimas_mediciones:
            velocidad = medicion.get('velocidad_kmh')
            medicion['exceso'] = velocidad and velocidad > limite_velocidad

        return JsonResponse({
            'estado': 'esperando_sensor2' if hay_pendiente else 'esperando_sensor1',
            'limite_velocidad': limite_velocidad,
            'ultimas_mediciones': ultimas_mediciones,
        })


class AutoView(View):
    """Vista reactiva que muestra JSON recibido desde la API."""
    template_name = 'dashboard/auto.html'

    def get(self, request):
        api_url = getattr(settings, 'FASTAPI_BASE_URL', 'http://localhost:8080')
        
        context = {
            'api_url': api_url,
        }
        return render(request, self.template_name, context)
