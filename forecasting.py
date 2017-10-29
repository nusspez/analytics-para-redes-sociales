from watson_developer_cloud import NaturalLanguageClassifierV1
import json


class Watson:
    def __init__(self,path_file):
        self.nlc = NaturalLanguageClassifierV1(
            username='005b0d1e-b254-469d-bb36-539ab440a7f7',
            password='1VDjW1OINtPX')
        self.id = 'ebd2f7x230-nlc-69615' #self.create_classifier(path_file)


    def create_classifier(self, path_file):
        with open(path_file, 'rb') as training_data:
            classifier = self.nlc.create(
                training_data=training_data,
                name='dardo_v4',
                language='es'
            )
        #return json.dumps(classifier, indent=4)
        return classifier['status']

    def wait_for_watson(self):
        while True:
            status = self.nlc.status(self.id)
            if status["status"] == "Available":
                return

    def classify(self, text, detail=False):
        classes = self.nlc.classify(self.id, text)

        if detail:
            copy = {
                "top_class": classes['top_class'],
                "classes": classes['classes']
            }
            return copy
        confidence = [c['confidence'] for c in classes['classes'] if c['class_name']==classes['top_class']][0]
        return classes['top_class'], confidence

path_file = '/home/kira/projects/analytics-para-redes-sociales/dataset.csv'

watson = Watson(path_file)
print(watson.classify("ando bien pudiente"))
