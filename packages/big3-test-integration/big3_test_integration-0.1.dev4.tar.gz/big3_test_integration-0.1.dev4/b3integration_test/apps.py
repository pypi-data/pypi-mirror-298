from b3integrations.abstract_classes import AbstractIntegrationAppConfig


class B3IntegrationTestConfig(AbstractIntegrationAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'b3integration_test'

    is_integration = True
