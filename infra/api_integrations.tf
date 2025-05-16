
resource "aws_apigatewayv2_route" "application_gateway_route" {
  api_id             = aws_apigatewayv2_api.application_gateway_api.id
  route_key          = "ANY /{proxy+}"
  target             = "integrations/${aws_apigatewayv2_integration.application_gateway_integration.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.lambda_authorizer.id
}

resource "aws_apigatewayv2_route" "public_docs_route" {
  api_id    = aws_apigatewayv2_api.application_gateway_api.id
  route_key = "GET /new_docs"
  target    = "integrations/${aws_apigatewayv2_integration.application_gateway_integration.id}"
}

resource "aws_apigatewayv2_route" "public_openapi_route" {
  api_id    = aws_apigatewayv2_api.application_gateway_api.id
  route_key = "GET /openapijson"
  target    = "integrations/${aws_apigatewayv2_integration.application_gateway_integration.id}"
}

resource "aws_apigatewayv2_vpc_link" "application_gateway_vpc_link" {
  name               = "application_gateway_vpc_link"
  security_group_ids = [aws_security_group.app_api_sg.id]
  subnet_ids         = ["${data.aws_subnet.private_subnet_1.id}", "${data.aws_subnet.private_subnet_2.id}"]
}

resource "aws_apigatewayv2_integration" "application_gateway_integration" {
  api_id           = aws_apigatewayv2_api.application_gateway_api.id
  credentials_arn  = data.aws_iam_role.lab_role.arn
  description      = "Load Balancer integration"
  integration_type = "HTTP_PROXY"
  integration_uri  = var.load_balancer_dns

  integration_method = "ANY"
  connection_type    = "VPC_LINK"
  connection_id      = aws_apigatewayv2_vpc_link.application_gateway_vpc_link.id

  response_parameters {
    status_code = 403
    mappings = {
      "append:header.auth" = "$context.authorizer.authorizerResponse"
    }
  }
}
