import cv2
from django.db import models
from .orb_recognition import extract_descriptors
from pickle import dumps, loads
from PIL import Image
from .nn_embeds import get_embedding


def front_cover_upload_to(instance, filename):
    return f"book/{instance.id}/front_cover.jpg"


def back_cover_upload_to(instance, filename):
    return f"book/{instance.id}/back_cover.jpg"


class Author(models.Model):

    first_name = models.CharField(
        verbose_name="First name",
        max_length=20,
        null=True,
        blank=True
    )

    last_name = models.CharField(
        verbose_name="Last name",
        max_length=20,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):

    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Book(models.Model):

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.is_available = self.user_set.count() < self.copies_available
        if self.front_cover and not self.descriptor_front:
            self.create_descriptors()
        if self.front_cover and not self.embed_front:
            self.genereate_embeddings()
        super().save(*args, **kwargs)

    def create_descriptors(self):
        front_cover = cv2.imread(self.front_cover.path)
        back_cover = cv2.imread(self.back_cover.path)
        self.descriptor_front = dumps(
            extract_descriptors(front_cover))
        self.descriptor_back = dumps(
            extract_descriptors(back_cover))

    title = models.CharField(
        verbose_name="Book title",
        max_length=50,
        null=True,
        blank=True
    )

    author = models.ForeignKey(
        Author,
        verbose_name="Author",
        on_delete=models.CASCADE
    )

    publisher = models.ForeignKey(
        Publisher,
        verbose_name="Publisher",
        on_delete=models.CASCADE
    )

    genre = models.ForeignKey(
        Genre,
        verbose_name="Genre",
        on_delete=models.CASCADE
    )

    front_cover = models.ImageField(
        verbose_name="Front cover",
        upload_to=front_cover_upload_to,
        null=True,
        blank=True
    )

    back_cover = models.ImageField(
        verbose_name="Back cover",
        upload_to=back_cover_upload_to,
        null=True,
        blank=True
    )

    copies_available = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    descriptor_front = models.BinaryField(null=True, blank=True)
    descriptor_back = models.BinaryField(null=True, blank=True)
    embed_front = models.BinaryField(null=True, blank=True)
    embed_back = models.BinaryField(null=True, blank=True)
    position = models.CharField(max_length=10, null=True, blank=True)

    def genereate_embeddings(self):
        front_cover = Image.open(self.front_cover.path)
        back_cover = Image.open(self.back_cover.path)
        self.embed_front = dumps(get_embedding(front_cover))
        self.embed_back = dumps(get_embedding(back_cover))

    def check_availability(self):
        self.is_available = self.user_set.count() < self.copies_available
        self.save()

    def __str__(self):
        return self.title
