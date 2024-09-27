from sparknlp.annotator import *

class SparkNLPAlbert:
    @staticmethod
    def get_default_model():
        return AlbertEmbeddings.pretrained() \
        .setInputCols("sentence", "token") \
        .setOutputCol("albert")

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        return AlbertEmbeddings.pretrained(name, language) \
            .setInputCols("sentence", "token") \
            .setOutputCol("albert")



