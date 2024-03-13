resource "aws_lambda_function" "backend_service" {
  function_name    = var.lambda_function_name 
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.8"
  timeout          = 30
  memory_size      = 128
  role             = aws_iam_role.lambda_execution_role.arn
  #source_code_hash = filebase64("./my_function/my_deployment_package.zip")
  filename = "./my_function/my_deployment_package.zip"


 depends_on = [ aws_iam_role_policy_attachment.lambda_execution_policy_attachment ]

}

output "arn" {
  value = aws_lambda_function.backend_service.arn
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role_demo"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_execution_policy_attachment" {
  for_each = toset([
       "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
       "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
       "arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole"
  ])
  policy_arn =  each.value
  role       = aws_iam_role.lambda_execution_role.name

   depends_on = [ aws_iam_role.lambda_execution_role ]

}

resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 1
}
