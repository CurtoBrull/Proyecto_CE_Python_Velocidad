#!/usr/bin/env python3
"""
Script para verificar el despliegue del sistema de radar de velocidad en Render.
Actualiza las URLs con las de tu despliegue real.
"""

import requests
import time
import json
import sys

# ⚠️ ACTUALIZA ESTAS URLs CON LAS DE TU DESPLIEGUE REAL
API_URL = "https://radar-velocidad-api-xxxx.onrender.com"  # Cambiar por tu URL del API
FRONTEND_URL = "https://radar-velocidad-frontend-yyyy.onrender.com"  # Cambiar por tu URL del frontend

def check_urls():
    """Verifica que las URLs estén actualizadas."""
    if "xxxx" in API_URL or "yyyy" in FRONTEND_URL:
        print("❌ ERROR: Debes actualizar las URLs en este script")
        print(f"API_URL actual: {API_URL}")
        print(f"FRONTEND_URL actual: {FRONTEND_URL}")
        print("\n📝 Instrucciones:")
        print("1. Ve a tu dashboard de Render")
        print("2. Copia las URLs reales de tus servicios")
        print("3. Actualiza las variables API_URL y FRONTEND_URL en este script")
        return False
    return True

def test_api_health():
    """Verifica que el API esté funcionando."""
    print("🔍 Verificando API...")
    try:
        response = requests.get(f"{API_URL}/mediciones/")
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            return True
        else:
            print(f"❌ API respondió con código {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al API: {e}")
        return False

def test_api_measurement():
    """Prueba crear mediciones en el API."""
    print("🧪 Probando creación de mediciones...")
    try:
        # Primera medición (incompleta)
        response1 = requests.post(f"{API_URL}/mediciones/")
        if response1.status_code != 200:
            print(f"❌ Error en primera medición: {response1.status_code}")
            return False
        
        print("⏳ Esperando 3 segundos...")
        time.sleep(3)
        
        # Segunda medición (completa)
        response2 = requests.post(f"{API_URL}/mediciones/")
        if response2.status_code != 200:
            print(f"❌ Error en segunda medición: {response2.status_code}")
            return False
        
        medicion = response2.json()
        if medicion.get("medicion_completa"):
            velocidad = medicion.get("velocidad_kmh", 0)
            print(f"✅ Medición completada - Velocidad: {velocidad:.2f} km/h")
            return True
        else:
            print("❌ La medición no se completó correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error probando mediciones: {e}")
        return False

def test_frontend():
    """Verifica que el frontend esté funcionando."""
    print("🌐 Verificando Frontend...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ Frontend funcionando correctamente")
            return True
        else:
            print(f"❌ Frontend respondió con código {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al Frontend: {e}")
        return False

def test_api_docs():
    """Verifica que la documentación del API esté disponible."""
    print("📚 Verificando documentación del API...")
    try:
        response = requests.get(f"{API_URL}/docs")
        if response.status_code == 200:
            print("✅ Documentación del API disponible")
            return True
        else:
            print(f"❌ Documentación no disponible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accediendo a documentación: {e}")
        return False

def main():
    """Ejecuta todas las pruebas."""
    print("🚀 Iniciando verificación del despliegue en Render")
    print("=" * 50)
    
    # Verificar que las URLs estén actualizadas
    if not check_urls():
        return False
    
    tests = [
        ("API Health Check", test_api_health),
        ("API Documentation", test_api_docs),
        ("API Measurements", test_api_measurement),
        ("Frontend Check", test_frontend),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Pruebas pasadas: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 ¡Despliegue verificado exitosamente!")
        print(f"🌐 Frontend: {FRONTEND_URL}")
        print(f"🔗 API: {API_URL}")
        print(f"📚 Docs: {API_URL}/docs")
        print("\n💡 Configuración para Arduino:")
        print(f"   POST {API_URL}/mediciones/")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los logs de Render.")
        print("\n🔍 Posibles causas:")
        print("- Los servicios están iniciándose (espera 1-2 minutos)")
        print("- Variables de entorno mal configuradas")
        print("- Problemas de CORS entre frontend y API")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)