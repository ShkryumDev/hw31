from rest_framework.fields import SerializerMethodField, BooleanField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from ads.models import Ad, Category, Selection
from ads.validators import not_true
from users.models import User


class AdSerializer(ModelSerializer):
    is_published = BooleanField(validators=[not_true], required=False)

    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(ModelSerializer):
    author_id = SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category_id = SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(ModelSerializer):
    author_id = SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category_id = SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    address = SerializerMethodField()

    def get_address(self, ad):
        return ad.author_id.username

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field='username', read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = ['name', 'items', 'owner', 'id']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
