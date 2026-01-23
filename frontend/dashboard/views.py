from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .api_client import RadarAPIClient


class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        client = RadarAPIClient()

        estadisticas = client.obtener_estadisticas()
        ultimas_mediciones = client.obtener_mediciones(limit=10)
        distancia = client.obtener_distancia()

        for medicion in ultimas_mediciones:
            velocidad = medicion.get('velocidad_kmh')
            medicion['exceso'] = velocidad and velocidad > 50

        context = {
            'estadisticas': estadisticas,
            'ultimas_mediciones': ultimas_mediciones,
            'distancia_actual': distancia,
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

        for medicion in mediciones:
            velocidad = medicion.get('velocidad_kmh')
            medicion['exceso'] = velocidad and velocidad > 50

        context = {
            'mediciones': mediciones,
            'page': page,
            'has_prev': page > 1,
            'has_next': len(mediciones) == limit,
            'fecha_inicio': fecha_inicio or '',
            'fecha_fin': fecha_fin or '',
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

        velocidad = medicion.get('velocidad_kmh')
        medicion['exceso'] = velocidad and velocidad > 50

        context = {'medicion': medicion}
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

        context = {
            'distancia_actual': distancia,
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

        return redirect('dashboard:configuracion')


class NuevaMedicionView(View):
    template_name = 'dashboard/nueva_medicion.html'

    def get(self, request):
        client = RadarAPIClient()
        distancia = client.obtener_distancia()

        context = {
            'distancia_actual': distancia,
            'estado': 'inicial',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        client = RadarAPIClient()
        accion = request.POST.get('accion')

        if accion == 'iniciar':
            result = client.registrar_medicion()
            if 'error' not in result:
                if result.get('es_primera_medicion'):
                    messages.info(request, 'Sensor 1 activado. Esperando paso por sensor 2...')
                else:
                    velocidad_kmh = result.get('velocidad_kmh', 0)
                    tiempo = result.get('tiempo_recorrido', 0)
                    if velocidad_kmh and velocidad_kmh > 50:
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
                messages.error(request, f'Error al registrar: {result["error"]}')

        return redirect('dashboard:nueva_medicion')
