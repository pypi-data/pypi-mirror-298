import random

class UzAi:
    def __init__(self):
        self.responses = []
        self.random_responses = []
        self.not_understood_response = None

    def question(self, question):
        self.question = question

    def response(self, responses):
        self.responses = responses

    def random_response(self, random_responses):
        self.random_responses = random_responses

    def not_response(self, not_understood_response):
        self.not_understood_response = not_understood_response

    def run(self):
        # Oddiy javoblar bilan tekshirish
        for response in self.responses:
            if self.question.lower() == response['ques'].lower():
                print(response['resp'])
                return

        # Tasodifiy javoblar bilan tekshirish
        for rand_resp in self.random_responses:
            if self.question.lower() == rand_resp['ques'].lower():
                possible_responses = rand_resp['ran_resp'].split('|')
                print(random.choice(possible_responses))
                return

        # Agar savolga mos javob topilmasa
        if self.not_understood_response:
            print(self.not_understood_response[0])

# Kutubxonani ishlatish
if __name__ == "__main__":
    ai = UzAi()
    savol = input('Savol kiriting: ')
    ai.question(savol)

    ai.not_response(['Savolingizga tushunmadim'])

    ai.random_response([
        {'ques': 'salom', 'ran_resp': 'Salom, qanday yordam bera olaman?|Salom, qalaysiz?|Salom, ishlar qalay?'},
        {'ques': 'qalaysan?', 'ran_resp': 'Yaxshi, o\'zingiz qalaysiz?|Yaxshiman, o\'zingiz yaxshimisiz?'}
    ])

    ai.run()
