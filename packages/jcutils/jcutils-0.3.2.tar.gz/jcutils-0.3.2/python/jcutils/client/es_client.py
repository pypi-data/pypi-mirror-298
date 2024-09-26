"""
Created on 2017/11/22 0022 17:31
@author: lijc210@163.com
Desc:
"""
import json
import traceback

from elasticsearch import Elasticsearch, NotFoundError, Urllib3HttpConnection, helpers

from src.config import CONFIG

ES_HOST = CONFIG.ES_HOST
SNIFF_ON_START = CONFIG.SNIFF_ON_START


class EsClient:
    def __init__(self, hosts=None, sniff_on_start=True):
        self.hosts = hosts
        self.sniff_on_start = sniff_on_start
        self.es_client = self.conn()

    def conn(self):
        """
        如果应用程序长时间运行，请考虑打开嗅探，以确保客户端在群集位置上是最新的,
        如果是测试环境，其中有些端口不通，请设置sniff_on_start=False
        :return:
        """
        return Elasticsearch(
            self.hosts,
            retry_on_timeout=True,
            timeout=100,
            max_retries=3,
            sniff_on_start=self.sniff_on_start,
            sniff_on_connection_fail=True,
            sniffer_timeout=60,
            sniff_timeout=1,
            request_timeout=30,
        )

    def get(self, index=None, doc_type=None, id=None, _source=None, params=None):
        """
        获取单条
        :param index:
        :param doc_type:
        :param body:
        :param params:
        :return:
        """
        try:
            if params:
                response = self.es_client.get(
                    index, id, doc_type=doc_type, _source=_source, params=None
                )
            else:
                response = self.es_client.get(
                    index, id, doc_type=doc_type, _source=_source
                )
            return response
        except NotFoundError:
            return None
        except Exception:
            traceback.print_exc()

    def mget(self, index=None, doc_type=None, body=None, params=None):
        """
        获取单条
        :param index:
        :param doc_type:
        :param body:
        :param params:
        :return:
        """
        if params:
            response = self.es_client.mget(
                body, index=index, doc_type=doc_type, params=None
            )
        else:
            response = self.es_client.mget(body, index=index, doc_type=doc_type)
        return response

    def search(self, index=None, doc_type=None, body=None, params=None):
        """
        搜索
        :param index:
        :param doc_type:
        :param body:
        :param params:
        :return:
        """
        if params:
            response = self.es_client.search(
                index=index, doc_type=doc_type, body=body, params=params
            )
        else:
            response = self.es_client.search(index=index, doc_type=doc_type, body=body)
        return response

    def index(self, index=None, doc_type=None, body=None, id=None, params=None):
        """
        覆盖文档内容
        :param index:
        :param doc_type:
        :param body:
        :param params:
        :return:
        """
        if params:
            response = self.es_client.index(index, doc_type, body, id=id, params=params)
        else:
            response = self.es_client.index(index, doc_type, body, id=id)
        return response

    def update(self, index=None, doc_type=None, body=None, id=None, params=None):
        """
        更新文档内容
        :param index:
        :param doc_type:
        :param body:
        :param params:
        :return:
        """
        if params:
            response = self.es_client.update(
                index, doc_type, id, body=body, params=params
            )
        else:
            response = self.es_client.update(index, doc_type, id, body=body)
        return response

    def mtermvectors(self, index=None, doc_type=None, body=None, params=None):
        """

        :param index:
        :param doc_type:
        :param body:
        :param params:
        :return:
        """
        if params:
            response = self.es_client.mtermvectors(
                index=index, doc_type=doc_type, body=body, params=params
            )
        else:
            response = self.es_client.mtermvectors(
                index=index, doc_type=doc_type, body=body
            )
        return response

    def bulk(self, actions=None, params=None, request_timeout=100, raise_on_error=True):
        """
        批量更新文档内容

        actions = [
            {
                '_op_type': 'index',
                '_index': 'test_index',
                '_type': 'test_type',
                '_id': 1,
                '_source': {'a': 'a', 'b': 'b'}
            },
            {
                '_op_type': 'index',
                '_index': 'test_index',
                '_type': 'test_type',
                '_id': 2,
                '_source': {'a': 'a', 'b': 'b'}
            },
        ]

        :param actions:
        :param params:
        :param request_timeout:
        :return:
        """
        if params:
            success, errors = helpers.bulk(
                self.es_client,
                actions=actions,
                request_timeout=request_timeout,
                raise_on_error=raise_on_error,
                params=params,
            )
        else:
            success, errors = helpers.bulk(
                self.es_client,
                actions=actions,
                request_timeout=request_timeout,
                raise_on_error=raise_on_error,
            )
        return success, errors

    def parallel_bulk(
        self, actions=None, params=None, request_timeout=100, raise_on_error=True
    ):
        """
        多线程批量更新文档内容

        actions = [
            {
                '_op_type': 'index',
                '_index': 'test_index',
                '_type': 'test_type',
                '_id': 1,
                '_source': {'a': 'a', 'b': 'b'}
            },
            {
                '_op_type': 'index',
                '_index': 'test_index',
                '_type': 'test_type',
                '_id': 2,
                '_source': {'a': 'a', 'b': 'b'}
            },
        ]

        :param actions:
        :param params:
        :param request_timeout:
        :return:
        """
        if params:
            success, errors = helpers.bulk(
                self.es_client,
                actions=actions,
                request_timeout=request_timeout,
                raise_on_error=raise_on_error,
                params=params,
            )
        else:
            success, errors = helpers.bulk(
                self.es_client,
                actions=actions,
                request_timeout=request_timeout,
                raise_on_error=raise_on_error,
            )
        return success, errors

    def delete(self, index, doc_type, id, params=None):
        try:
            if params:
                return self.es_client.delete(index, doc_type, id, params)
            return self.es_client.delete(index, doc_type, id)
        except NotFoundError:
            return False
        except Exception:
            traceback.print_exc()

    def delete_by_query(self, index=None, doc_type=None, body=None, params=None):
        try:
            if params:
                return self.es_client.delete_by_query(
                    index, body, doc_type=doc_type, params=None
                )
            return self.es_client.delete_by_query(index, body, doc_type=doc_type)
        except Exception:
            traceback.print_exc()
            return False

    def scan(
        self,
        index=None,
        doc_type=None,
        body=None,
        scroll="5m",
        raise_on_error=True,
        preserve_order=False,
        size=5000,
        request_timeout=None,
        clear_scroll=True,
        **kwargs,
    ):
        """
        获取所有文档
        :param
        :return:
        """

        response = helpers.scan(
            self.es_client,
            index=index,
            doc_type=doc_type,
            query=body,
            scroll=scroll,
            raise_on_error=raise_on_error,
            preserve_order=False,
            size=size,
            request_timeout=request_timeout,
            clear_scroll=clear_scroll,
            **kwargs,
        )
        return response

    def analyze(self, index, analyzer, text):
        return self.es_client.indices.analyze(
            index=index,
            body={"text": text, "analyzer": analyzer},
            params={"filter": ["lowercase"]},
        )


class MyConnection(Urllib3HttpConnection):
    def __init__(self, *args, **kwargs):
        extra_headers = kwargs.pop("extra_headers", {})
        super().__init__(*args, **kwargs)
        self.headers.update(extra_headers)


class EsClient6(EsClient):
    def __init__(self, hosts):
        EsClient.__init__(self, hosts)

    def conn(self):
        return Elasticsearch(
            hosts=self.hosts,
            connection_class=MyConnection,
            retry_on_timeout=True,
            timeout=100,
            max_retries=3,
            extra_headers={"Content-Type": "application/json"},
        )


if __name__ == "__main__":
    es_client = EsClient(ES_HOST, sniff_on_start=SNIFF_ON_START)
    # #######get#######
    response = es_client.get(index="zxtt", doc_type="note_new", id=121246)
    print(json.dumps(response, ensure_ascii=False))

    #######search#######
    # body = {
    #     "query": {},
    #     "sort": [
    #         {
    #             "create_time": {
    #                 "order": "desc"
    #             }
    #         }
    #     ], "_source": ["title"]
    # }
    # response = es_client.search(index="aabb", doc_type="v9_news", body=body, params=None)
    # print json.dumps(response,ensure_ascii=False)

    # ######index#######
    # body = {"id": 21254600, "title": "兼具座椅与置物功能的脚凳，不仅样子小巧，在视觉上消减了家具体...",
    #  "content": "[{\"type\":1,\"text\":\"兼具座椅与置物功能的脚凳，不仅样子小巧，在视觉上消减了家具体量，而且放个托盘就可以替代茶几的功能了，移动起来非常方便，能够灵活满足生活中的多种需求。\"},{\"type\":2,\"url\":\"https://imgmall.tg.com.cn/zmzx/2018/7/10/846/3458f55d-ef49-4baf-a53e-79b616f292f6.jpg\",\"width\":1000,\"height\":750},{\"type\":2,\"url\":\"https://imgmall.tg.com.cn/zmzx/2018/7/10/846/dbf2970e-07b1-4f9e-ba9c-db5e099a95c0.jpg\",\"width\":664,\"height\":481},{\"type\":2,\"url\":\"https://imgmall.tg.com.cn/zmzx/2018/7/10/846/e271fa85-ee1d-42bb-a46b-ae9cde901dc4.jpg\",\"width\":768,\"height\":614},{\"type\":2,\"url\":\"https://imgmall.tg.com.cn/zmzx/2018/7/10/846/610553e3-0850-4310-b4ff-1beba63354f8.jpg\",\"width\":1000,\"height\":750}]",
    #  "link_url": 0, "link_text": 0, "link_icon_url": 0, "verify_status": 1, "status": 1, "user_id": 105367818,
    #  "user_name": "深圳漾设计", "community_master_id": 2, "community_second_id": 0, "is_top": 0, "is_recommend": 0,
    #  "virtual_support_count": 0, "comment_count": 4, "type": 4, "vote_id": 0, "video_id": 0,
    #  "refuse_reason_id": 0, "refuse_reason": 0, "reject_time": 0, "create_time": 1531184903000,
    #  "update_time": 1531437285000, "last_comment_time": 1531437285000, "is_up": 0, "is_down": 0, "is_locked": 0,
    #  "source_id": 108176, "source_type": 114}
    #
    # response = es_client.index(index="zxtt", doc_type="note_new", body=body, id=21254600, params=None)
    # print json.dumps(response,ensure_ascii=False)

    # #######bulk#######

    # actions = [
    #     {
    #         '_op_type': 'index',
    #         '_index': 'test_index',
    #         '_type': 'test_type',
    #         '_id': 1,
    #         '_source': {'a': 'a', 'b': 'b'}
    #     },
    #     {
    #         '_op_type': 'index',
    #         '_index': 'test_index',
    #         '_type': 'test_type',
    #         '_id': 2,
    #         '_source': {'a': 'a', 'b': 'b'}
    #     },
    # ]
    #
    # actions = [
    #     {
    #         '_op_type': 'index',
    #         '_index': 'ask_v1',
    #         '_type': 'zd_topic',
    #         '_id': 305958,
    #         '_source': {
    #             "zd_topic_id": 305958,
    #             "app_id": 100,
    #             "q_id": "583695034718685645",
    #             "title": "室内设计师这个职业怎么样",
    #             "content":
    #             "室内设计师需要学什么专业\n工资怎么样？\n前景怎么样？\n什么样的人不适合做？\n室内设计师是干什么的呀？",
    #             "poster_name": "匿名",
    #             "userid": None,
    #             "create_time": 1420270771,
    #             "view_num": 27,
    #             "upload_status": 0,
    #             "reply_counts": 1,
    #             "tag_one_id": 70,
    #             "tag_two_id": None,
    #             "tag_one_name": None,
    #             "tag_two_name": None,
    #             "accepted_reply_id": None,
    #             "status": 2,
    #             "modify_time": 1531964956,
    #             "is_accepted": 1,
    #             "q_type": None,
    #             "client_ip": None,
    #             "zx_type": None,
    #             "pic_urls": "[]",
    #             "source": None
    #         }
    #     },
    # ]
    #
    # success, errors = es_client.bulk(actions=actions)
    # print success, errors

    #######scan#######
    # body = {
    #     "query": {
    #         "bool": {
    #             "must_not": [
    #                 {
    #                     "term": {
    #                         "check_status": {
    #                             "value": "-1"
    #                         }
    #                     }
    #                 }
    #             ],
    #             "filter": [
    #                 {
    #                     "range": {
    #                         "answer_count": {
    #                             "gt": 0
    #                         }
    #                     }
    #                 }
    #             ]
    #         }
    #     },
    #     "_source": [
    #         "id",
    #         "create_time",
    #         "answer_count"
    #     ]
    # }
    # response = es_client.scan(index="zxtt", doc_type="question", body=body)
    # import time
    #
    # question_pkey_time = {}
    # zd_topic_unzero_answer = {}
    # for resp in response:
    #     if "_source" in resp:
    #         _id = resp["_source"]["id"]
    #         _create_time = resp["_source"]["create_time"]
    #         _answer_count = resp["_source"]["answer_count"]
    #         question_pkey_time[('zxtt.question-' + str(_id)).decode()] = time.mktime(
    #             time.strptime(_create_time, '%Y-%m-%d %H:%M:%S'))
    #         zd_topic_unzero_answer[id] = _answer_count
    # print question_pkey_time
    # print zd_topic_unzero_answer

    #######delete_by_query#######
    # print es_client.delete_by_query(index="cut_word_data", doc_type="wap_anli.article-content", body={"query": {}})

    #######update#######
    # body = {"doc": {u'up_time': 1541671205L, u'good_comment_num': 71L, u'preview_num': 147L,
    #                 'mongo_id': '5be40890a4186af01f4434e2', u'is_today': 1L, u'tag': [u'64', u'48', u'15'],
    #                 u'is_check': 3L,
    #                 u'is_online': 2L, u'nopass_reason': u''}
    #         }
    # response = es_client.update(index="decoration_v1", doc_type="shop_case", body=body, id=281657, params=None)
    # print json.dumps(response, ensure_ascii=False)
    pass
