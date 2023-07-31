# rest-framework imports
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_404_NOT_FOUND,
)
from .serializers import (
    BuildingSerializer,
    ElevatorSerializer,
    RequestSerializer,
    RequestSerializer2
)

# django imports
from django.shortcuts import render
from django.db.models import Q, Func, F
from django.db import transaction
from .models import Building, Elevator, Request


# A function to check existance of object if exist then return [True,object] else return [False,None]
def check_exist(obj, id):
    # filtering object with id

    obj_list = obj.objects.filter(id=id)
    if obj_list.exists():
        return True, obj_list[0]
    return False, None


class BuildingAPI(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    # overiding default create method of ModelViewSet to create objects of Elevator as a object of Building created
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = BuildingSerializer(data=data)
            if serializer.is_valid():
                with transaction.atomic():
                    serializer.save()
                    building = serializer.instance
                    # creating objects of elevator
                    for i in range(1, (int(data["no_of_elevators"]) + 1)):
                        elevator = Elevator.objects.create(
                            building=building, current_floor=0, elevator_no=i
                        )
                        elevator.save()
                    return Response({"data": serializer.data}, status=200)
            return Response(
                {
                    "status": 406,
                    "message": "Enter valid data",
                },
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        except Exception:
            return Response(
                {
                    "status": 404,
                    "message": "Something  went wrong try again.",
                },
                status=HTTP_404_NOT_FOUND,
            )


# An elevator api in ModelViewSet
class ElevatorAPI(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer


# An request api to call most optimal elevator
class RequestAPI(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    # Overriding default create method to use own logic
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = RequestSerializer2(data=data)
            if serializer.is_valid():
                # A floor from request sent
                current_floor = int(data["current_floor"])
                # A destination floor of request
                destination_floor = int(data["destination_floor"])
                # Checking requested  building exist
                exist, building = check_exist(Building, data["building"])
                if exist:
                    # Checking that the value of current floor and destination floor must be less than no of floors in buildings
                    if (
                        current_floor <= building.no_of_floors
                        and destination_floor <= building.no_of_floors
                    ):
                        # Desiding the direction of request
                        if current_floor < destination_floor:
                            direction = "up"
                        else:
                            direction = "down"
                        with transaction.atomic():
                            elevators = Elevator.objects.select_for_update().filter(
                                working_status="working"
                            )
                            # Optimal elevator assingment start here
                            # Fetching elevator according to its direction
                            if direction == "up":
                                elevators_fi = elevators.select_for_update().filter(
                                    Q(status=direction)
                                    & Q(current_floor__lte=current_floor)
                                )
                            else:
                                elevators_fi = elevators.select_for_update().filter(
                                    Q(status=direction)
                                    & Q(current_floor__gte=current_floor)
                                )

                            if not elevators_fi.exists():
                                elevators_fi = elevators.select_for_update().filter(
                                    status="stoped"
                                )

                            # The following logic call nearest elevator
                            elevator = (
                                elevators_fi.annotate(
                                    abs_diffrance=Func(
                                        F("current_floor") - current_floor,
                                        function="ABS",
                                    )
                                )
                                .order_by("abs_diffrance")
                                .first()
                            )
                            # The following logic call nearest elevator if all elevators are busy
                            if elevator is None:
                                user_requests = (
                                    Request.objects.select_for_update().filter(
                                        status="ongoing"
                                    )
                                )
                                closest_request = (
                                    user_requests.annotate(
                                        abs_diffrance=Func(
                                            F("destination_floor") - current_floor,
                                            function="ABS",
                                        )
                                    )
                                    .order_by("abs_diffrance")
                                    .first()
                                )
                                elevator = closest_request.elevator
                            serializer.save()
                            # Assigning closest elevator to request
                            serializer.instance.direction = direction
                            serializer.instance.elevator = elevator
                            serializer.instance.save()
                            # Changin elevator status
                            elevator.status = direction
                            elevator.save()
                            return Response(data=serializer.data, status=HTTP_200_OK)

                    return Response(
                        {
                            "status": 406,
                            "message": f"Current floors or Destination floors must be less than  {building.no_of_floors} ",
                        },
                        status=HTTP_406_NOT_ACCEPTABLE,
                    )
                return Response(
                    {
                        "status": 406,
                        "message": "Enter valid building id",
                    },
                    status=HTTP_406_NOT_ACCEPTABLE,
                )
            return Response(
                {
                    "status": 406,
                    "message": "Enter valid data",
                },
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        except Exception:
            return Response(
                {
                    "status": 404,
                    "message": "Something  went wrong try again.",
                },
                status=HTTP_404_NOT_FOUND,
            )


# API to change door status of elevator
class ChangeDoorAPI(APIView):
    # A patch request is used because we are updating only one field of elevator object
    def patch(self, request):
        try:
            data = request.data
            if data["id"] is not None:
                try:
                    # Fetching elevator and changing its door status
                    id = int(data["id"])
                    with transaction.atomic():
                        elevator = Elevator.objects.select_for_update().get(id=id)
                        if elevator.door_status == "open":
                            elevator.door_status = "close"
                        else:
                            elevator.door_status = "open"
                        elevator.save()
                        serializer = ElevatorSerializer(elevator)

                        return Response(
                            {
                                "status": 200,
                                "message": "door status changed successfully",
                                "data": serializer.data,
                            },
                            status=HTTP_200_OK,
                        )
                except Exception:
                    return Response(
                        {
                            "status": 406,
                            "message": "id must be an integer",
                        },
                        status=HTTP_406_NOT_ACCEPTABLE,
                    )
            return Response(
                {
                    "status": 406,
                    "message": "id is required",
                },
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        except Exception:
            return Response(
                {
                    "status": 404,
                    "message": "Something  went wrong try again.",
                },
                status=HTTP_404_NOT_FOUND,
            )

# Home page
def index(request):
    return render(request,'app/index.html')