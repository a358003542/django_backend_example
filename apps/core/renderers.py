import json
from collections import OrderedDict
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ErrorDetail
from .nested_dict import nested_dict, nested_dict_from_dict

def explainErrorDetail(data):
    """
    """
    for key, value in data.items():
        if isinstance(value, dict):
            explainErrorDetail(value)
        elif isinstance(value, ErrorDetail):
            data[key] = {
                'detail': str(value),
                'code': value.code
            }

    return data


class ConduitJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'objects'
    pagination_count_label = 'count'

    def render(self, data, media_type=None, renderer_context=None):
        if data.get('results', None) is not None:
            ret_data = {
                self.pagination_object_label: data['results'],
                self.pagination_count_label: data['count']
            }
            renderer_context['response'].data = ret_data
            return super(ConduitJSONRenderer, self).render(ret_data,
                                                           accepted_media_type=media_type,
                                                           renderer_context=renderer_context)

        # NOTICE 异常结果返回应该是 {'errors': ... } 如果不是则程序有误
        elif data.get('errors', None) is not None:

            ret_data = explainErrorDetail(data)
            renderer_context['response'].data = ret_data
            return super(ConduitJSONRenderer, self).render(ret_data,
                                                            accepted_media_type=media_type,
                                                            renderer_context=renderer_context)
        # 正常结果返回格式
        else:
            ret_data = {
                self.object_label: data
            }

            res = nested_dict()
            nested_dict_from_dict(ret_data, res)
            ret_data = res.to_dict()

            # testcase need this modification
            renderer_context['response'].data = ret_data
            return super(ConduitJSONRenderer, self).render(ret_data,
                                                           accepted_media_type=media_type,
                                                           renderer_context=renderer_context)

class UploadJSONRenderer(ConduitJSONRenderer):
    object_label = 'upload'
    pagination_object_label = 'uploads'
    pagination_count_label = 'uploadsCount'