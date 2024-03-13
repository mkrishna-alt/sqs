module "lambda_fun" {
  source = "../lambda"
}

resource "aws_sqs_queue" "terraform_queue" {
  name                      = "terraform-main-queue"
  delay_seconds             = 0
  visibility_timeout_seconds = 30
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.terraform_queue_deadletter.arn
    maxReceiveCount     = 4
  })


  tags = {
    Environment = "production"
  }
}

resource "aws_sqs_queue" "terraform_queue_deadletter" {
  name = "terraform-example-fallback-queue"
}

resource "aws_lambda_event_source_mapping" "example_lambda_sqs_trigger" {
  event_source_arn = aws_sqs_queue.terraform_queue.arn
  function_name    = module.lambda_fun.arn

 
}
resource "aws_lambda_event_source_mapping" "example_lambda_sqs_trigge_dead_letter" {
  event_source_arn = aws_sqs_queue.terraform_queue_deadletter.arn
  function_name    = module.lambda_fun.arn

   
  }
output "lambda_config" {
  value = module.lambda_fun.arn
}