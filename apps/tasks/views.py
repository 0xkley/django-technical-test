from django.utils import timezone
from django_filters import rest_framework as django_filters
from django import forms
from django.http import Http404
from django.conf import settings

from drf_spectacular.utils import extend_schema, OpenApiExample

from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound

from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer

class TaskFilter(django_filters.FilterSet):
  due_date_from = django_filters.DateTimeFilter(
    field_name = "due_date", 
    lookup_expr = "gte",

    #* Descripción para documentación Swagger
    label = "Fecha de vencimiento desde (ej: 2026-08-13T00:00:00Z)",
  )

  due_date_to = django_filters.DateTimeFilter(
    field_name = "due_date",
    lookup_expr = "lte",
    label = "Fecha de vencimiento hasta (ej: 2026-08-13T00:00:00Z)"
  )

  class Meta:
    model = Task
    fields = ["status", "due_date_from", "due_date_to"]

  def clean(self):
    cleanned_data = super().clean()
    date_from = cleanned_data.get("due_date_from")
    date_to = cleanned_data.get("due_date_to")

    if date_from and date_to and date_from > date_to:
      raise forms.ValidationError("due_date_from no puede ser mayor a due_date_to")

    return cleanned_data


class TaskViewSet(ModelViewSet):
  serializer_class = TaskSerializer

  filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
  filterset_class = TaskFilter
  search_fields = ["title", "description"]

  def get_object(self):
    try:
      return super().get_object()
    except Http404:
      task_id = self.kwargs.get("pk")
      raise NotFound(detail=f"La tarea con id {task_id} no existe o fue eliminada")

  @extend_schema(
    summary = "Crear tarea",
    description = (
      "Crea una nueva tarea. 'due_date' debe ser una fecha futura. "
      "'title' y 'created_by_name' son obligatorios."
    ),
  )
  def create(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)

  def get_queryset(self):
    return Task.objects.filter(
      deleted_at__isnull = True
    )

  @extend_schema(
    summary = "Eliminar tarea",
    description = (
      "Elimina una tarea de forma lógica, actualizando 'deleted_at' de NULL a un valor. "
      "Si 'deleted_at' tiene una fecha o valor diferente a NULL, se tomará como tarea eliminada. "
    ),
  )
  def destroy(self, request, *args, **kwargs):
    task = self.get_object()

    task.deleted_at = timezone.now()
    task.save(
      update_fields = ["deleted_at", "updated_at"]  
    )

    return Response(
      status = status.HTTP_204_NO_CONTENT,
    )

  @extend_schema(
    summary = "Cambiar el estado de una tarea",
    description = (
      "Actualiza únicamente el campo 'status' de una tarea existente, "
      "ignora los demás campos aunque sean enviados. "
      "Valores enumerados o permitidos: pending (pendiente), completed (completada), postponed (pospuesta)."
    ),
    request = TaskStatusUpdateSerializer,
    responses = TaskSerializer,
    examples = [
      OpenApiExample(
        "Marcar como completada",
        value = {"status": "completed"},
        request_only = True,
      ),
    ],
  )
  @action(detail=True, methods=["patch"], url_path="status")
  def change_status(self, request, pk=None):
    task = self.get_object()

    serializer = TaskStatusUpdateSerializer(
      task, 
      data = request.data, 
      partial = True,
    )
    serializer.is_valid(raise_exception = True)
    serializer.save()

    return Response(
      TaskSerializer(task).data,
      status = status.HTTP_200_OK
    )

  @extend_schema(
    summary = "Listar tareas que estén cerca de su fecha de vencimiento",
    description = (
      "Lista las tareas (no completadas ni eliminadas) que tienen una fecha de vencimiento "
      "cercanas o dentro del limite del criterio predefinido de horas (48 horas) desde el momento de la consulta."
      "El criterio no es modificable y está definido en el README.md y archivo .env"
    ),
    responses = TaskSerializer(many=True),
  )
  @action(detail=False, methods=["get"], url_path="upcoming")
  def upcoming(self, request):
    within_hours = settings.UPCOMING_HOURS_LIMIT # criterio de horas próximas a vencer
    limit = timezone.now() + timezone.timedelta(hours=within_hours)

    tasks = self.get_queryset().filter(
      due_date__lte = limit
    ).exclude(
      status = Task.TaskStatus.COMPLETED
    )

    serializer = self.get_serializer(tasks, many=True)
    return Response(serializer.data)

