1. 验证AAD issuer的access_token，需要注意的几个点：

   1. add_token_verify 在python lib中显示只支持到 python3.9,用python3.11测试下来也没有什么大问题，只是因为它的认证点是v1版本
      和目前的v2版本不匹配。如果修改成v1去request access_token，那个issuer是一个固定值，后面校验也没有办法通过。

      ```
      @cached(cache=TTLCache(maxsize=16, ttl=3600))
      def _get_openid_config(tenant_id: str) -> Dict[str, Any]:
          """Retrieves the OpenID config for a specified issuer

          Args:
              tenant_id (str): The tenant id of the issuer

          Returns:
              Dict[str, Any]: The OpenID config
          """
          oidc_response = requests.get(f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration")
          oidc_response.raise_for_status()
          return oidc_response.json()
      ```
2. 在配置请求access_token的参数的时候，如果scope配置成https://graph.microsoft.com/.default的话，证书校验会一直失败。

   这个通过与产品组讨论，目前就是这样，微软公共的scope，客户都不能用来校验证书。

   ```
   payload = {
           "grant_type": "client_credentials",
           "client_id": client_id,
           "client_secret": client_secret,
           "scope": "api://cd5347aa-d60d-49f7-9877-e036b25c9f94/.default"}

   ```
3. 如果想要正确验证的话，需要两个app register，一个是客户端，一个接收端（audience)。 同时scope也就是audience对应的url，正确格式：api://cd5347aa-d60d-49f7-9877-e036b25c9f94/.default
4. 在app service中配置audience 和scope的话，需要开启Authetication
<img width="831" alt="Screenshot 2024-05-29 at 17 37 04" src="https://github.com/huqianghui/access_token_validate_poc/assets/7360524/600a7af1-9b68-4ad8-844e-41499711ca0c">
