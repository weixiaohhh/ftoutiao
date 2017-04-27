import datetime
from haystack import indexes
from .models import Article


class PostIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	create_time = indexes.DateTimeField(model_attr='create_time')
	author = indexes.CharField(model_attr='author')

	def get_model(self):
		return Article

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(create_time__lte=datetime.datetime.now())
