from mock import Mock, patch

from nefertari.view import BaseView
from nefertari_guards.view import ACLFilterViewMixin


class TestACLFilterViewMixin(object):
    @patch('nefertari_guards.view.ACLFilterES')
    def test_get_collection_es_auth_enabled(self, mock_es):
        class View(ACLFilterViewMixin, BaseView):
            pass

        request = Mock(content_type='', method='', accept=[''])
        view = View(
            context={}, request=request,
            _query_params={'foo': 'bar'})
        view._auth_enabled = True
        view.Model = Mock(__name__='MyModel')
        view._query_params['q'] = 'movies'
        result = view.get_collection_es()
        mock_es.assert_called_once_with('MyModel')
        mock_es().get_collection.assert_called_once_with(
            q='movies', foo='bar', request=request)
        assert result == mock_es().get_collection()
