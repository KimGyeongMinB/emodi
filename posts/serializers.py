from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "author_nickname", "author", "view_count"]

    def create(self, validated_data):
        user = self.context.get('request').user
        return Post.objects.create(author=user, **validated_data)
    
    def get_author_nickname(self, obj):
        return obj.author.nickname if obj.author else None
    
    def get_view_count(self, obj):
        return getattr(obj, "view_count", 0)
    
    def update(self, instance, validated_data):
        user = self.context.get('request').user
        if user != instance.author:
            raise serializers.ValidationError("작성자만 삭제할수 있습니다.")

        instance.tags = validated_data.get('tags', instance.tags)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("제목은 3자 이상입니다.")
        if not value:
            raise serializers.ValidationError("제목을 입력해주세요.")
        
        return value
    
    def validate_content(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("본문의 내용을 1자 이상 입력해주세요")
        if not value:
            raise serializers.ValidationError("본문을 입력해주세요.")
        
        return value