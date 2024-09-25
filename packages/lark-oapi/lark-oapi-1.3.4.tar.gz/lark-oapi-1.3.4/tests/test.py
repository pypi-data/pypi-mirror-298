import io
import asyncio

from requests_toolbelt import MultipartEncoder

import lark_oapi
import lark_oapi as lark
from lark_oapi.api.im.v1 import *


def test():
    # SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
    # 以下示例代码是根据 API 调试台参数自动生成，如果存在代码问题，请在 API 调试台填上相关必要参数后再使用
    # 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
    def main():
        # 创建client
        client = lark.Client.builder() \
            .app_id("cli_a5d1921ef9d3500b") \
            .app_secret("GAmmmAMgI4UXYZyGMDqfAevPRVHrR6T1") \
            .build()
            # .log_level(lark.LogLevel.DEBUG) \

        # 构造请求对象
        request: CreateMessageRequest = CreateMessageRequest.builder() \
            .receive_id_type("open_id") \
            .request_body(CreateMessageRequestBody.builder()
                          .receive_id("ou_7d8a6e6df7621556ce0d21922b676706cc11")
                          .msg_type("text")
                          .content("{\"text\":\"test content\"}")
                          .uuid("a0d69e20-1dd1-458b-k525-dfeca4015204")
                          .build()) \
            .build()

        # 发起请求
        response: CreateMessageResponse = client.im.v1.message.create(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, error response: {lark.JSON.marshal(response.error)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    main()


def run_async_function(sync_callback):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(sync_callback)

def upload_all_file(file):
    # print(isinstance(io.BufferedReader, io.IOBase))
    # return
    # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a3aacb5fdf78d00e") \
        .app_secret("2zwKfrqM2xe9kMjoz2OmIgmUFUB7CAeH") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象

    data = {
        "name": "2305.14283.pdf",
        "type": "attachment",
        # "file_name": "2305.14283.pdf",
        # "parent_type": "explorer",
        # "parent_node": "FHsUf2I0wl8oscdH46dcDsKNn0c",
        # "size": 1212451,
        # "file":  ("2305.14283.pdf", file, "")
        "content": ("2305.14283.pdf", file, "")
    }
    body = MultipartEncoder(lark.Files.parse_form_data(data))

    # request: lark.BaseRequest = (lark.BaseRequest.builder() \
    #     .http_method(lark.HttpMethod.POST) \
    #     .uri("/open-apis/drive/v1/files/upload_all") \
    #     .headers({"Content-Type": body.content_type}) \
    #     .token_types({lark.AccessTokenType.USER}) \
    #     .body(body) \
    #     .build())

    request: lark.BaseRequest = (
        lark.BaseRequest.builder()
        .http_method(lark.HttpMethod.POST)
        .uri("/approval/openapi/v2/file/upload")
        .headers({"Content-Type": body.content_type})
        .token_types({lark.AccessTokenType.TENANT})
        .body(body)
        .build()
    )

    # 发起请求
    response: lark.BaseResponse = client.request(request, option=lark_oapi.RequestOption.builder().user_access_token("u-fTy552b6N2.XXUMGUCED1Nh0iqsBh1f1V0G0ghC821fU").build())

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.request failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(str(response.raw.content, lark.UTF_8))

if __name__ == '__main__':
    test()
    # file = open("/Users/bytedance/Downloads/2305.14283.pdf", "rb")
    # file = open("/Users/bytedance/Downloads/2c60da4397e18c0ae1fdf6bf50b36ad4_gvIc3W7D2z.png", "rb")
    # upload_all_file(file)
