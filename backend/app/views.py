from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import get_result


class DetectLocationAPIView(APIView):
    def post(self, request):
        _locations = request.data.get("locations")
        locations = [l["location"] for l in _locations]
        print(locations)
        """
         "40.6233,48.6543",
            "41.1952,47.1973",
            "40.6556,47.7466",
            "39.2206,45.4395",
            "40.1051,46.0396","""
        _result = sorted(
            get_result(locations), key=lambda x: x["data"]["efficiency"], reverse=True
        )
        return Response(data=_result, status=HTTP_200_OK)
