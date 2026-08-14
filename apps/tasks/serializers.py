from django.utils import timezone
from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = [
      "id",
      "title",
      "description",
      "status",
      "due_date",
      "created_at",
      "updated_at",
      "created_by_name",
      "deleted_at",
    ]
    read_only_fields = [
      "id",
      "created_at",
      "updated_at",
      "deleted_at",
    ]


  def validate_title(self, value):
    value = value.strip()

    if not value:
      raise serializers.ValidationError(
        "El título no puede estar vacío"
      )

    return value

  def validated_created_by_name(self, value):
    value = value.strip()

    if not value:
      raise serializers.ValidationError(
        "El nombre del usuario no puede estar vacío"
      )
  

  def validate_due_date(self, value):
    if value < timezone.now():
      raise serializers.ValidationError(
        "Fecha de vencimiento inválida"
      )

    return value



class TaskStatusUpdateSerializer(serializers.ModelSerializer):
  status = serializers.ChoiceField(
    choices = Task.TaskStatus.choices,
    error_messages = {
      "invalid_choice": "Estado inválido. Valores permitido: pending, completed, postponed."
    },
  )

  class Meta:
    model = Task
    fields = ["status"]