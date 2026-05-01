output "data_lake_bucket" {
  description = "Name of the S3 bucket used for the data lake."
  value       = aws_s3_bucket.data_lake.bucket
}
