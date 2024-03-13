

module "sqs_service" {
  source = "./sqs"
}

module "dynamo_db" {
  source = "./dynamo"
}

