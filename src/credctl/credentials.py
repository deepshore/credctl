from kubernetes import client, config


class NamespaceDoesNotExistError(Exception):
    pass


class CannotConfigureClientError(Exception):
    pass


class CredentialsSecret:
    def __init__(self, namespace='default', kubeconfig=None):
        try:
            config.load_kube_config(kubeconfig)
        except config.ConfigException:
            raise CannotConfigureClientError(
                'Cannot configure kubernetes python client'
            )

        self.core_v1 = client.CoreV1Api()

        namespaces_list = self.core_v1.list_namespace()
        namespaces = [item.metadata.name for item in namespaces_list.items]
        if namespace in namespaces:
            self.namespace = namespace
        else:
            raise NamespaceDoesNotExistError('Namespace does not exist.')

        self.labels = {
            'managed-by': 'credctl',
        }

    @staticmethod
    def __is_managed_by_credctl(secret):
        try:
            if secret.metadata.labels['managed-by'] == 'credctl':
                return True
            return False
        except (TypeError, KeyError):
            return False

    def __get_secret_body(self, name, username, password):
        return client.V1Secret(
            metadata=client.V1ObjectMeta(
                name=name,
                labels=self.labels
            ),
            string_data={
                'username': username,
                'password': password
            }
        )

    def create(self, name, username, password):
        try:
            self.core_v1.create_namespaced_secret(
                namespace=self.namespace,
                body=self.__get_secret_body(name, username, password)
            )
            return 'Secret \'{name}\' with credentials was created.'.format(
                name=name
            )
        except client.ApiException as e:
            if e.reason == 'Conflict':
                return 'Secret \'{name}\' already exists.'.format(
                    name=name
                )

    def delete(self, name):
        try:
            secret = self.core_v1.read_namespaced_secret(
                name=name,
                namespace=self.namespace
            )
        except client.ApiException as e:
            if e.reason == 'Not Found':
                return 'Secret \'{name}\' not found.'.format(name=name)

        except Exception as e:
            return 'Something went wrong while deleting ' \
                   'secret \'{name}\'.'.format(name=name)

        if self.__is_managed_by_credctl(secret):
            self.core_v1.delete_namespaced_secret(
                name=name,
                namespace=self.namespace
            )

            return 'Secret \'{name}\' was deleted.'.format(name=name)
        else:
            return 'Secret \'{name}\' is not managed by credctl. ' \
                   'Deletion canceled.'.format(name=name)

    def list(self):
        secrets_list = self.core_v1.list_namespaced_secret(
            namespace=self.namespace,
            label_selector='managed-by=credctl'
        )
        secrets_names = [item.metadata.name for item in secrets_list.items]

        if secrets_names:
            secrets_str = '\n'.join(secrets_names)
            return 'Secrets managed by credctl in namespace ' \
                   '\'{namespace}\':\n{secrets}\n'.format(
                namespace=self.namespace,
                secrets=secrets_str
            )
        else:
            'There are no secrets managed by credctl ' \
            'in namespace \'{namespace}\''.format(namespace=self.namespace)


if __name__ == '__main__':
    # Use something similar for developing your code
    cs = CredentialsSecret(namespace='default')
    print(cs.list())
