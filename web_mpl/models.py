from django.core.validators import MinValueValidator
from django.db import models

class MplFigure(models.Model):
	fig_id = models.IntegerField(validators=[MinValueValidator(0)])