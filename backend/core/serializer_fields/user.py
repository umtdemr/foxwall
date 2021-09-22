from rest_framework.fields import Field


class IsFollowingField(Field):
    def __init__(self, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super(IsFollowingField, self).__init__(**kwargs)

    def to_representation(self, value):
        request = self.context.get('request')

        print(request)

        # if not request.user.is_anonymous:
        #     if request.user.pk == value.pk:
        #         return False
        #     return request.user.is_following_user_with_id(value.pk)

        return False
