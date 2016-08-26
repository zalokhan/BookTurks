from django.test import TestCase, Client

from service.bookturks.adapters import UserAdapter, QuizAdapter, QuizTagAdapter
from service.tests.constants_models import context
from service.tests.create_user import create_user


class QuizTagAdapterTest(TestCase):
    """
    Test case for the Quiz Tags Adapter
    """

    def setUp(self):
        """
        Initialization for all tests
        :return:
        """
        self.user_adapter = UserAdapter()
        self.quiz_adapter = QuizAdapter()
        self.quiz_tag_adapter = QuizTagAdapter()

    def test_create_model(self):
        """
        Testing the create model method
        :return: Asserts
        """
        client = Client()
        create_user()
        client.login(username=context.get('username'), password=context.get('password'))

        # Create and save user
        user = self.user_adapter.create_and_save_model(username=context.get('username'),
                                                       first_name=context.get('user_first_name'),
                                                       last_name=context.get('user_last_name'),
                                                       phone=context.get('user_phone'),
                                                       dob=context.get('user_dob'))

        # Create and save quiz with the above user as owner.
        quiz_model = self.quiz_adapter.create_and_save_model(quiz_id="quiz_id",
                                                             quiz_name="quiz_name",
                                                             quiz_description="quiz_description",
                                                             quiz_owner=user)

        # No tag exists.
        self.assertEqual(self.quiz_tag_adapter.exists("test_tag"), None)

        # Verify name
        self.assertEqual(self.quiz_tag_adapter.verify_tag_name("test?tag"), None)
        self.assertNotEqual(self.quiz_tag_adapter.verify_tag_name("test_tag"), None)

        # Creating tag
        test_tag = self.quiz_tag_adapter.create_model("test_tag")
        # Should not be able to link the tag to the quiz as it has not been saved yet.
        self.assertRaises(ValueError, self.quiz_tag_adapter.link_quiz,
                          tag_name=test_tag.tag_name,
                          quiz_id=quiz_model.quiz_id)

        test_tag = self.quiz_tag_adapter.create_and_save_model("test_tag")
        # No links yet
        self.assertEqual(quiz_model.quiztag_set.count(), 0)

        # Linking
        self.quiz_tag_adapter.link_quiz(tag_name=test_tag.tag_name,
                                        quiz_id=quiz_model.quiz_id)

        self.assertEqual(quiz_model.quiztag_set.count(), 1)
        # Checking whether tag linked to the right quiz.
        self.assertNotEqual(quiz_model.quiztag_set.all()[0], None)
        self.assertEqual(test_tag.tagged_quiz.all()[0], quiz_model)

        self.quiz_tag_adapter.unlink_quiz(quiz_id=quiz_model.quiz_id,
                                          tag_name=test_tag.tag_name)
        self.assertEqual(self.quiz_tag_adapter.exists(test_tag.tag_name), None)
