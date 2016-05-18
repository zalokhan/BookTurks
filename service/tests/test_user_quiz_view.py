from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from service.tests.create_user import create_user, context


class UserQuizViewTest(TestCase):
    """
    Test case for the Quiz pages
    """

    def test_user_quiz_init_view(self):
        """
        Testing the user quiz view
        :return: Asserts
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quiz_init'), context)
        self.assertEqual(response.status_code, 200)

    def test_user_quiz_maker_view_with_valid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        quiz_parameters = dict(context)

        quiz_parameters['quiz_id'] = 'test_quiz_id'
        quiz_parameters['quiz_name'] = 'test_quiz_name'
        quiz_parameters['quiz_description'] = 'test_quiz_description'

        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))
        response = client.post(reverse('service:user_quiz_maker'), quiz_parameters)
        self.assertEqual(response.status_code, 200)

    def test_user_quiz_verifier_view_with_null_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), context, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_both_invalid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = 'garbage'
        quiz_parameters['quiz_form'] = 'garbage'
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_form_invalid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = '<form-template>\r\n\t<fields>\r\n\t\t<field class="header" label="Header" ' \
                                       'type="header" subtype="h1"></field>\r\n\t</fields>\r\n</form-template>'
        quiz_parameters['quiz_form'] = "garbage"
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_logically_invalid_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = '<form-template>\r\n\t<fields>\r\n\t\t<field class="header" label="Header" ' \
                                       'type="header" subtype="h1"></field>\r\n\t</fields>\r\n</form-template>'
        # <from > instead of <form>
        quiz_parameters['quiz_form'] = '<div id="rendered-form" style="padding-top: 40px; display: block;">\r\n    ' \
                                       '<from action="#"><div class=""><h1>Header</h1></div></form>\r\n    ' \
                                       '<button class="btn btn-default edit-form">Edit</button>\r\n</div>'
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_less_inputs(self):
        """
        Testing the user maker quiz view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = '<form-template>\r\n\t<fields>\r\n\t\t<field class="header" label="Header" ' \
                                       'type="header" subtype="h1"></field>\r\n\t</fields>\r\n</form-template>'
        # <from > instead of <form>
        quiz_parameters['quiz_form'] = '<div id="rendered-form" style="padding-top: 40px; display: block;">\r\n    ' \
                                       '<form action="#"><div class=""></div></form>\r\n    ' \
                                       '<button class="btn btn-default edit-form">Edit</button>\r\n</div>'
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_verifier_view_with_valid_inputs(self):
        """
        Testing the user maker quiz view with valid inputs
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['quiz_data'] = '<form-template>\r\n\t<fields>\r\n\t\t<field class="header" label="Header" ' \
                                       'type="header" subtype="h1"></field>\r\n\t</fields>\r\n</form-template>'
        quiz_parameters['quiz_form'] = '<div id="rendered-form" style="padding-top: 40px; display: block;">\r\n    ' \
                                       '<form action="#"><div class=""><h1>Header</h1></div></form>\r\n    ' \
                                       '<button class="btn btn-default edit-form">Edit</button>\r\n</div>'
        # Testing response status code
        response = client.post(reverse('service:user_quiz_verifier'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        self.assertEqual(response.redirect_chain, redirect_chain)

    def test_user_quiz_create_view_with_all_invalid_inputs(self):
        """
        Testing create view
        :return:
        """
        client = Client()
        user = create_user()
        self.assertEqual(user.is_active, True)
        client.login(username=context.get('username'), password=context.get('password'))

        # Preparing the context
        quiz_parameters = dict(context)
        quiz_parameters['answer_key'] = {'answer_key': 'test'}
        # Testing response status code
        response = client.post(reverse('service:user_quiz_create'), quiz_parameters, follow=True)
        self.assertEqual(response.status_code, 200)
        # Testing redirection
        redirect_chain = list()
        redirect_chain.append(("/quiz/init/", 302))
        self.assertEqual(response.redirect_chain, redirect_chain)
