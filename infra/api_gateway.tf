
resource "aws_apigatewayv2_api" "application_gateway_api" {
  name          = "application_gateway_api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "application_gateway_stage" {
  api_id      = aws_apigatewayv2_api.application_gateway_api.id
  name        = "dev"
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.auth_api_stage_log_group.arn
    format = jsonencode({
      "requestId"      = "$context.requestId",
      "ip"             = "$context.identity.sourceIp",
      "requestTime"    = "$context.requestTime",
      "httpMethod"     = "$context.httpMethod",
      "routeKey"       = "$context.routeKey",
      "status"         = "$context.status",
      "protocol"       = "$context.protocol",
      "responseLength" = "$context.responseLength"
    })
  }
}

resource "aws_cloudwatch_log_group" "auth_api_stage_log_group" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.application_gateway_api.name}"

  retention_in_days = 14
}

resource "aws_apigatewayv2_authorizer" "lambda_authorizer" {
  api_id                            = aws_apigatewayv2_api.application_gateway_api.id
  authorizer_type                   = "REQUEST"
  authorizer_uri                    = data.aws_lambda_function.authorizer.invoke_arn
  identity_sources                  = ["$request.header.Authorization"]
  name                              = "lambda_authorizer"
  authorizer_payload_format_version = "2.0"
  enable_simple_responses           = true
}
