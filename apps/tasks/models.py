import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Task(models.Model):
  class TaskStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    COMPLETED = "completed", "Completada"
    POSTPONED = "postponed", "Pospuesta"

  id = models.UUIDField(
    primary_key = True,
    default = uuid.uuid4,
    editable = False
  )

  title = models.CharField(
    max_length=200,
  )

  description = models.TextField(
    blank = True,
    default = "",
  )

  status = models.CharField(
    max_length = 20,
    choices = TaskStatus.choices,
    default = TaskStatus.PENDING,
  )

  due_date = models.DateTimeField()

  created_by_name = models.CharField(
    max_length = 150,
  )

  created_at = models.DateTimeField(
    auto_now_add = True,
  )

  updated_at = models.DateTimeField(
    auto_now = True,
  )

  deleted_at = models.DateTimeField(
    null = True,
    blank = True,
    default = None,
  )

  class Meta:
    db_table = "tasks"
    ordering = ["due_date", "-created_at"]
    indexes = [
      models.Index(fields=["status"]),
      models.Index(fields=["due_date"]),
      models.Index(fields=["deleted_at"]),
    ]

  def __str__(self):
    return self.title

  