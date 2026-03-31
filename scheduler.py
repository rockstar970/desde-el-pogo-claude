import schedule
import time
from main import main

# Corre todos los días a las 9:00 AM (hora Argentina = UTC-3)
# En Railway, el servidor corre en UTC, así que 9 AM Argentina = 12:00 UTC
schedule.every().day.at("12:00").do(main)

# También a las 6 PM Argentina = 21:00 UTC (doble cobertura)
schedule.every().day.at("21:00").do(main)

print("⏰ Scheduler iniciado. Corriendo a las 9:00 AM y 6:00 PM (hora Argentina)")
print("   Próxima ejecución:", schedule.next_run())

# Correr una vez al inicio para verificar que todo funciona
print("\n🚀 Corriendo una vez ahora para verificar...\n")
main()

while True:
    schedule.run_pending()
    time.sleep(60)
