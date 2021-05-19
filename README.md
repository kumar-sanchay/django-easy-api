# django-easy-api

Now there is no need to create apis for common CRUD operation for any model.
By using `django-easy-api` its really easy. Kindly follow the below steps for including this library into your project.

1. Create Your django project.

2. Add `easy_api` in settings.py
```python
INSTALLED_APPS = [
	.
	.
	.
	'easy_api'
]
```

3. Create your django app

4. Now in models.py follow create your model by inheriting EasyAPI model from easy_api app.
```python

from django.db import models
from easy_api.models import EasyAPI

class MyModel(EasyAPI):
	# Your Requried field here.
```

5. Migrate your models.

6. This is the last step. You need to add this model in your app's urls.py
```python
from django.urls import path
from .models import MyModel

urlpatterns = [
	path('myurl/', MyModel.as_view()),
]
```

7. That's it. Now you will have common GET/POST/PUT/DELETE methods on your model.
Also you can attach query_params only for `id` in your url.
For example:

```
http://localhost:8000/myurl/?id=1
```

8. You can also override get, post, put and delete method according to your need.
For example:
```python

from django.db import models
from easy_api.models import EasyAPI

class MyModel(EasyAPI):
	# Your Requried field here.
	
	def get(self, request):
		#Your logic
```


