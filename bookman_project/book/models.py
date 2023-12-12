from django.db import models


def front_cover_upload_to(instance, filename) :
	return f"book/{instance.id}/front_cover.jpg"

def back_cover_upload_to(instance, filename) :
	return f"book/{instance.id}/back_cover.jpg"


class Author(models.Model) :

	first_name = models.CharField(
		verbose_name = "First name",
		max_length = 20,
		null = True,
		blank = True
	)

	last_name = models.CharField(
		verbose_name = "Last name",
		max_length = 20,
		null = True,
		blank = True
	)

	def __str__(self) :
		return f"{self.first_name} {self.last_name}"

class Publisher(models.Model) :

	name = models.CharField(
		verbose_name = "Name",
		max_length = 50,
		null = True,
		blank = True
	)

	def __str__(self) :
		return self.name

class Genre(models.Model) :

	name = models.CharField(
		verbose_name = "Name",
		max_length = 50,
		null = True,
		blank = True
	)

	def __str__(self) :
		return self.name

class Book(models.Model) :

	title = models.CharField(
		verbose_name = "Book title",
		max_length = 50,
		null = True,
		blank = True
	)

	author = models.ForeignKey(
		Author,
		verbose_name = "Author",
		on_delete = models.CASCADE
	)

	publisher = models.ForeignKey(
		Publisher,
		verbose_name = "Publisher",
		on_delete = models.CASCADE
	)

	genre = models.ForeignKey(
		Genre,
		verbose_name = "Genre",
		on_delete = models.CASCADE
	)

	front_cover = models.ImageField(
		verbose_name = "Front cover",
		upload_to = front_cover_upload_to,
		null = True,
		blank = True
	)

	back_cover = models.ImageField(
		verbose_name = "Back cover",
		upload_to = back_cover_upload_to,
		null = True,
		blank = True
	)

	def __str__(self) :
		return self.title