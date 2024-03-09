# Overview of sqs

* Unlimited throughput and msg queue
* SQS is an oldest server in AWS cloud
* Maximum msg size 256KB
* Retention min 4 days max 14 days
* msg Can be duplicated ( at least once delivary)

Visibility timeout 
* delay the prcess of consuming 0 to 12 hr

Long Polling 
* Once consumer request for queue, it can wait for the period of time for any msg to arrive.
* Decreses the number of API calls made SQS
* Wiating time between 1 sec to 20 sec.

FIFO
* exactly once delivery 
* But limite in throufhgput 300 m/s or 3000 m/s if its a batching
