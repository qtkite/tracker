from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from track.models import Record
from track.serializer import RecordSerializer
import time


class GetAllRecords(generics.ListAPIView):
    """
    Returns all records
    """
    queryset = Record.objects.all()
    serializer_class = RecordSerializer


class GetActiveRecord(APIView):
    """
    Gets the current active record from the current login
    """

    def get(self, request, format=None):
        user = request.user
        existing = Record.objects.filter(uid=user.id, is_active=True)
        if len(existing) > 0:
            # an existing one exists, lets return that instead
            latest = RecordSerializer(existing[0])
            return Response(latest.data, status=status.HTTP_200_OK)

        # we need to create a new record and return that instead
        temp = {"created": int(time.time()), "ended": 0,
                "uid": user.id, "is_active": True}
        serializer = RecordSerializer(data=temp)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddRecord(APIView):
    """
    Adds a new record, given one doesn't already exists
    """

    def post(self, request, format=None):
        user = request.user

        existing = Record.objects.filter(uid=user.id, is_active=True)
        if len(existing) > 0:
            return Response({"status": "existing record already exists"},
                            status.HTTP_400_BAD_REQUEST)

        temp = {"created": int(time.time()), "ended": 0,
                "uid": user.id, "is_active": True}
        serializer = RecordSerializer(data=temp)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetRecord(APIView):
    """
    Disables the latest record and assigns a new one

    to-do:
    set the ended time
    """

    def get(self, request, format=None):
        user = request.user

        existing = Record.objects.filter(uid=user.id, is_active=True)
        for record in existing:
            record.is_active = False
            record.save(update_fields=['is_active'])

        # assign a new record and save it
        temp = {"created": int(time.time()), "ended": 0,
                "uid": user.id, "is_active": True}
        serializer = RecordSerializer(data=temp)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DisableAllRecords(APIView):
    """
    Sets all existing records as not active
    """

    def get(self, request, format=None):
        all_records = Record.objects.all()
        for record in all_records:
            record.is_active = False
            record.save(update_fields=["is_active"])
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
