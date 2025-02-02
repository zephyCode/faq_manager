# models.py
from django.db import models
from django.core.cache import cache
from ckeditor.fields import RichTextField
from googletrans import Translator

class Faq(models.Model):
    question = models.TextField()
    answer = RichTextField(config_name='default')
    question_hi = models.TextField(blank=True, null=True)
    answer_hi = models.TextField(blank=True, null=True)
    question_esp = models.TextField(blank=True, null=True)
    answer_esp = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    CACHE_TIMEOUT = 60 * 60 * 24
    
    def get_cache_key(self, content_type, lang):
        return f"faq_translation_{self.id}_{content_type}_{lang}"
    
    def get_cached_translation(self, text, dest_lang, content_type):
        if not text:
            return None
            
        cache_key = self.get_cache_key(content_type, dest_lang)
        cached_translation = cache.get(cache_key)

        # print(type(cached_translation))
        # print(text)
        
        # if cached_translation:
        #     return cached_translation
            
        try:
            translator = Translator()
            translated_text = translator.translate(text, dest=dest_lang).text
            if translated_text and translated_text.strip():
                cache.set(cache_key, translated_text, self.CACHE_TIMEOUT)
                return translated_text
            return None
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            if not self.question_hi or not self.question_hi.strip():
                self.question_hi = self.get_cached_translation(
                    self.question, 'hi', 'question'
                )
            if not self.question_esp or not self.question_esp.strip():
                self.question_esp = self.get_cached_translation(
                    self.question, 'es', 'question'
                )
                
            if not self.answer_hi or not self.answer_hi.strip():
                self.answer_hi = self.get_cached_translation(
                    self.answer, 'hi', 'answer'
                )
            if not self.answer_esp or not self.answer_esp.strip():
                self.answer_esp = self.get_cached_translation(
                    self.answer, 'es', 'answer'
                )
        
        else:
            original = Faq.objects.get(pk=self.pk)
            if (original.question != self.question or 
                original.answer != self.answer):
                self.clear_translations_cache()
                
        super(Faq, self).save(*args, **kwargs)
    
    def clear_translations_cache(self):
        languages = ['hi', 'es']
        content_types = ['question', 'answer']
        
        for lang in languages:
            for content_type in content_types:
                cache_key = self.get_cache_key(content_type, lang)
                cache.delete(cache_key)
    
    def get_translated_content(self, lang='en'):
        """Get translated content with English fallback"""
        if lang == 'en':
            return {
                "question": self.question,
                "answer": self.answer
            }
            
        translations = {
            "hi": {
                "question": (self.question_hi if self.question_hi and self.question_hi.strip() 
                           else self.question),
                "answer": (self.answer_hi if self.answer_hi and self.answer_hi.strip() 
                         else self.answer)
            },
            "es": {
                "question": (self.question_esp if self.question_esp and self.question_esp.strip() 
                           else self.question),
                "answer": (self.answer_esp if self.answer_esp and self.answer_esp.strip() 
                         else self.answer)
            }
        }
        
        return translations.get(lang, {
            "question": self.question,
            "answer": self.answer
        })

    def __str__(self):
        return self.question