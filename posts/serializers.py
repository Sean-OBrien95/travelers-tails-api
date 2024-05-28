from rest_framework import serializers
from posts.models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('File size larger than 2MB!')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'location',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'video',
            'like_id', 'likes_count', 'comments_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Check if either image or video is present.
        """
        if not data.get('image') and not data.get('video'):
            raise serializers.ValidationError(
                "Either image or video is required.")
        return data

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        is_image_uploaded = validated_data.get('image')
        is_video_uploaded = validated_data.get('video')

        if is_image_uploaded:
            instance.video = None

        elif is_video_uploaded:
            instance.image = None

        instance.save()
        return instance
