class UserProfileModel(object):
    """
    Contains the User Profile.
    Do not store objects here.
    """

    def __init__(self, user_model=None, display_picture=None, attempted_quiz=None, my_quiz=None, notifications=None):
        # User Model
        self.user_model = user_model
        # Display picture
        self.display_picture = display_picture
        # List of quizzes attempted (quiz result models)
        self.attempted_quiz = attempted_quiz
        # List of my quizzes
        self.my_quiz = my_quiz
        # List of Notifications
        self.notifications = notifications

    def __str__(self):
        return "User : {0} \n" \
               "Display Picture : {1} \n" \
               "Attempted quizzes : {2} \n" \
               "My quizzes : {3} \n" \
               "Notifications : {4}".format(str(self.user_model),
                                            self.display_picture,
                                            [str(quiz_result_model) for quiz_result_model in self.attempted_quiz],
                                            [str(quiz) for quiz in self.my_quiz],
                                            [str(notification) for notification in self.notifications])
