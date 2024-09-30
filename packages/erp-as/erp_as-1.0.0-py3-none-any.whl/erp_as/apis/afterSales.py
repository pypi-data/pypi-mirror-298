from typing import Optional
from erp_as.erpRequest import Request
from erp_as.utils.util import dumps, getDefaultParams, JTable1


def AftersaleRequest(data: dict, method: str = 'LoadDataToJSON',
                 url: str = '/app/Service/aftersale/aftersale.aspx', **kwargs) -> Request:
    params = getDefaultParams({'defaultParams': ["ts___"], 'am___': method})
    if kwargs.get('params'):
        params.update(kwargs.get('params'))
    return Request(
        method='POST',
        url=url,
        params=params,
        data={
            **data
        },
        callback=JTable1
    )


# 获取售后退货退款订单
def aftersaleList(queryData: Optional[list] = None, page_num: int = 1, page_size: int = 500):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []
    return AftersaleRequest({
        '_jt_page_size': page_size,
        "__CALLBACKID": "JTable1",
        '__CALLBACKPARAM': dumps(
            {
                "Method": "LoadDataToJSON",
                "Args": [
                    page_num,
                    dumps(queryData),
                    "{}"
                ]
            }
        ),
    },
        method='LoadDataToJSON',
        params={'archive': 'false'}
    )


# 确认售后订单
def aftersaleCommon(afterIds):
    '''
    确认售后订单
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return AftersaleRequest({
        'isCB': '0',
        '__CALLBACKID': 'ACall1',
        '__CALLBACKPARAM': dumps(
            {
                "Method": "Confirms",
                "Args": [','.join(str(element) for element in afterIds), "false", "true", "false", "false", "false"],
             "CallControl": "{page}"
            }
        ),
    },
        method='Confirms',
        url='/app/Service/aftersale/aftersale_common.aspx'
    )

# 反确认售后订单
def unconfirms(afterIds):
    '''
    反确认售后订单
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return AftersaleRequest({
        'isCB': '0',
        '__CALLBACKID': 'ACall1',
        '__CALLBACKPARAM': dumps(
            {
                "Method": "UnConfirms",
                "Args": afterIds,
             "CallControl": "{page}"
            }
        ),
    },
        method='UnConfirms',
        url='/app/Service/aftersale/aftersale_common.aspx'
    )

# 确认收到退货
def confirmReturnQty(afterIds):
    '''
    反确认售后订单
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return AftersaleRequest({
        'isCB': '0',
        '__CALLBACKID': 'ACall1',
        '__CALLBACKPARAM': dumps(
            {
                "Method": "ConfirmReturnQty",
                "Args": afterIds,
             "CallControl": "{page}"
            }
        ),
    },
        method='ConfirmReturnQty',
        url='/app/Service/aftersale/aftersale_common.aspx'
    )

# 确认收到货物
def confirmGoods(afterIds):
    '''
    反确认售后订单
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return AftersaleRequest({
        'isCB': '0',
        '__CALLBACKID': 'ACall1',
        '__CALLBACKPARAM': dumps(
            {
                "Method": "ConfirmGoods",
                "Args": afterIds,
             "CallControl": "{page}"
            }
        ),
    },
        method='ConfirmGoods',
        url='/app/Service/aftersale/aftersale_common.aspx'
    )


# 更新售后单 售后类型
def save(update_orders):
    '''
    反确认售后订单
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return AftersaleRequest({
        'isCB': '0',
        '__CALLBACKID': 'JTable1',
        '__CALLBACKPARAM': dumps(
            {
                "Method": "Save",
                "Args": update_orders
            }
        ),
    },
        method='Save',
        url='/app/Service/aftersale/aftersale.aspx'
    )


# 售后单转转成
def clearException(afterIds):
    '''
    售后单转转成
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return AftersaleRequest({
        '__CALLBACKID': 'JTable1',
        '__CALLBACKPARAM': dumps({"Method":"ClearException","Args":afterIds,"CallControl":"{page}"}),
    },
        method='ClearException')


def getSkus(as_id):
    return AftersaleRequest({
        '__CALLBACKID': 'JTable1',
        '__CALLBACKPARAM': dumps({"Method":"GetSkus","Args":[as_id,False],"CallControl":"{page}"}),
    },
    method='GetSkus')










