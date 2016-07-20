
from django.http.response import JsonResponse

import app.models
import json

class controller():
    def query(request):
        # data = json.dumps(app.models.ChangeLog.objects.all())
        return JsonResponse({"total":28,"rows":[{"productid":"FI-SW-01","productname":"Koi","unitcost":10.00,"status":"P","listprice":36.50,"attr1":"Large","itemid":"EST-1"}]})

