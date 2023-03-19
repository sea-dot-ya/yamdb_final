import csv
import logging
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews import models as md
from users.models import User

logger = logging.getLogger(__name__)

DATA_PATH = os.path.join(settings.BASE_DIR, "static/data")

FILES_MODELS = {
    "users.csv": get_user_model(),
    "category.csv": md.Category,
    "genre.csv": md.Genre,
    "titles.csv": md.Title,
    "genre_title.csv": md.GenreTitle,
    "review.csv": md.Review,
    "comments.csv": md.Comments,
}


class Command(BaseCommand):
    help = "Загрузка данных из csv файлов."

    def handle(self, *args, **options):
        for file_name in FILES_MODELS:
            file_path = os.path.join(DATA_PATH, file_name)
            model = FILES_MODELS.get(file_name)
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    category = row.get("category")
                    author = row.get("author")
                    pub_date = row.get("pub_date")

                    if category:
                        row["category"] = md.Category.objects.get(pk=category)
                    if author:
                        row["author"] = User.objects.get(pk=author)
                    if pub_date:
                        row.pop("pub_date")

                    try:
                        logger.info(model.objects.get_or_create(**row))
                    except Exception:
                        logger.error(file_path, model, row, exc_info=True)
