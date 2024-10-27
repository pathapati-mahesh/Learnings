def new_game(**kwargs):
    print(kwargs['solutions'])
    guess=0
    correct_guess=[]
    default_question=1
    for question in kwargs['questions']:
        print("---------------------------------------------")
        print(question)

        for options in kwargs['solutions'][default_question-1]:
            print(options)
    default_question+=1
def check_answer():
    pass
def display_score():
    pass
def play_again():
    pass


questions={
    "Who is the father of Python ?:":"B",
    "Who is the father of Mathametics ?:":"A"
}
solutions=[["A.P Mahesh Kumar","B.Guido Van Russom","C.Onkar","D.Manas"],["A.P Mahesh","B.Srinivasa Ramanujan","C.Onkar","D.Manas"]]
new_game(questions=questions,solutions=solutions)
