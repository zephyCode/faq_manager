from rest_framework import serializers
from .models import Faq

class FaqSerializer(serializers.ModelSerializer):
    translated_content = serializers.SerializerMethodField()
    
    class Meta:
        model = Faq
        fields = ['id', 'question', 'answer', 'question_hi', 'answer_hi', 
                 'question_esp', 'answer_esp', 'translated_content']
        read_only_fields = ['question_hi', 'answer_hi', 'question_esp', 'answer_esp']

    def get_translated_content(self, obj):
        request = self.context.get('request')
        lang = request.GET.get('lang', 'en') if request else 'en'
        content = obj.get_translated_content(lang)
        return {
            "question": content.get("question") or obj.question,
            "answer": content.get("answer") or obj.answer,
            "language": lang,
            "has_translation": bool(
                (lang == 'hi' and obj.question_hi and obj.answer_hi) or
                (lang == 'es' and obj.question_esp and obj.answer_esp) or
                lang == 'en'
            )
        }

    def validate_question(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Question cannot be empty")
        return value.strip()

    def validate_answer(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Answer cannot be empty")
        return value.strip()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        translations = ['question_hi', 'answer_hi', 'question_esp', 'answer_esp']
        for field in translations:
            if not data.get(field):
                data[field] = None
                
        return data

    def create(self, validated_data):
        for field in ['question_hi', 'answer_hi', 'question_esp', 'answer_esp']:
            validated_data.pop(field, None)
            
        instance = Faq.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        for field in ['question_hi', 'answer_hi', 'question_esp', 'answer_esp']:
            validated_data.pop(field, None)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance