# implementacion para busquedas
from rest_framework import viewsets
from .models import Client
from .serializer import ClientSerializer
from datetime import datetime  # Para manejar fechas
from types import NoneType


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtra los registros de usuarios que no han sido marcados como borrados lógicamente.
        queryset = queryset.filter(deleted__exact=False)

        search = self.request.query_params.get('search', None)

        if search and not search.replace("-", "").isdigit():
            queryset = queryset.filter(full_name__icontains=search)

        elif search and search.replace("-", "").isdigit():
            try:
                count = search.count("-")
                searchComplete = search
                search = search.replace("-","")

                if len(search) == 4:  # 2023
                    queryset = queryset.filter(
                        creation_date__year=datetime.strptime(search,'%Y').date().year
                    )
                elif len(search) == 5 and search[-1] == "0":  # 20230
                    queryset = queryset.filter(
                        creation_date__year=datetime.strptime(search.rstrip('0'),'%Y').date().year
                    )
                elif len(search) == 5 or len(search) == 6: #20206 o 202006
                    queryset = queryset.filter(
                        creation_date__year=datetime.strptime(search,'%Y%m').date().year,
                        creation_date__month=datetime.strptime(search,'%Y%m').date().month
                    )
                elif len(search) == 6 and search[-1] == "0" and count == 2: # 2023-6-0
                    queryset = queryset.filter(
                        creation_date__year=datetime.strptime(search.rstrip("0"),'%Y%m').date().year,
                        creation_date__month=datetime.strptime(search.rstrip("0"),'%Y%m').date().month
                    )
                elif len(search) == 6 and search[-1] != "0" and count == 2: # 2023-6-5
                    queryset = queryset.filter(
                        creation_date__year=datetime.strptime(search,'%Y%m%d').date().year,
                        creation_date__month=datetime.strptime(search,'%Y%m%d').date().month,
                        creation_date__day=datetime.strptime(search, '%Y%m%d').date().day
                    )
                elif len(search) == 7 and search[-1] == "0" : #2023-05-0
                    queryset=queryset.filter(
                        creation_date__year=datetime.strptime(search.rstrip("0"),'%Y%m').date().year,
                        creation_date__month=datetime.strptime(search.rstrip("0"),'%Y%m').date().month
                    )
                elif len(search) == 7 or len(search) == 8 : #2023-05-04 o 2023-5-12
                    # Convertir el string en un objeto date
                    searchComplete = datetime.strptime(searchComplete, '%Y-%m-%d').date()
                    queryset = queryset.filter(creation_date=searchComplete)
                elif len(search) < 4:  # 202 -> Proporcionamos toda la información de la tabla
                    queryset = super().get_queryset()
                else:
                    queryset = queryset.none()
            except ValueError:
                # La cadena proporcionada no es una fecha válida
                queryset = queryset.none()

        return queryset