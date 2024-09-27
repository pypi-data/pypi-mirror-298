import sys

sys.path.append("../src")

# list all the modules
import pkgutil
import redflagbpm

for importer, modname, ispkg in pkgutil.iter_modules(redflagbpm.__path__):
    print("Found submodule %s (is a package: %s)" % (modname, ispkg))

from redflagbpm.BPMService import BPMService
from redflagbpm.MSSQLUtils import get_connection, fetch_dicts

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bpm = BPMService()

    with get_connection(bpm, 'MY_DB') as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT viaje,tviaje,peso
                    FROM [SAP].[dbo].[OF_CV_VIAJES]
                    WHERE tviaje = %s
                """,('RESERVAS',))
                result = fetch_dicts(cursor)
                for row in result:
                    print(row)
        except Exception as e:
            print("Error:", e)
