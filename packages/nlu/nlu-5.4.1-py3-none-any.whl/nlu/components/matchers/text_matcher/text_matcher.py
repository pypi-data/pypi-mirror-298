import sparknlp
from sparknlp.annotator import TextMatcherModel
class TextMatcher:
    @staticmethod
    def get_default_model():
        return sparknlp.annotator.TextMatcher() \
            .setInputCols("sentence","token") \
            .setOutputCol("matched_entity")


    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        return sparknlp.annotator.TextMatcherModel.pretrained(name,language,bucket) \
            .setInputCols("sentence","token") \
            .setOutputCol("matched_entity") \


